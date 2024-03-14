"""
Runs the release checklist.
"""

import html
import os

from datetime import datetime
from string import Template

import webbrowser
import wx

from src.app_data import AppData

import tests

from tests.unit_tests.test_checklist import view_checklist
from tests.unit_tests.test_checklist.view_checklist import ViewCheckList


ITEMS = [
    {"label": "All issues in GitHub fixed", "type": bool, "pass_if": True, "result": None},
    {"label": "All unit tests passed", "type": bool, "pass_if": True, "result": None},
    {"label": "All test configuration runs passed", "type": bool, "pass_if": True, "result": None},
    {"label": "Duration test passed", "type": bool, "pass_if": True, "result": None},
    {"label": "Correct version in AppData", "type": bool, "pass_if": True, "result": None},
    {"label": "Documentation up to date", "type": bool, "pass_if": True, "result": None},
    {"label": "Set tag in git", "type": bool, "pass_if": True, "result": None},
    {"label": "Create deployment", "type": bool, "pass_if": True, "result": None},
    {"label": "Publish deployment on LilyTronics", "type": bool, "pass_if": True, "result": None},
    {"label": "Publish deployment on GitHub", "type": bool, "pass_if": True, "result": None}
]
REPORT_TIME_STAMP_FORMAT = "%Y%m%d_%H%M%S"
REPORT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def _get_result_for_item(item, check):
    result = f"unknown type: {item["type"]}"
    if item["type"] is bool:
        if item["pass_if"] == check.GetValue():
            result = "PASSED"
        else:
            result = "FAILED"
    return result


def check_callback(checks, remarks, open_in_browser):
    now = datetime.now()
    timestamp = now.strftime(REPORT_TIME_STAMP_FORMAT)

    template_values = {
        "start_message": f"Release checklist for application version: V{AppData.VERSION}",
        "date": now.strftime(REPORT_DATE_FORMAT),
        "result": "",
        "result_class": "",
        "result_message": "",
        "checklist_results": ""
    }

    results = '<table class="results">\n'
    results += '<tr><th>Test</th><th class="center">Result</th><th>Remarks</th>\n'
    n_passed = 0
    for i, item in enumerate(ITEMS):
        result = _get_result_for_item(item, checks[i])
        if result == "PASSED":
            n_passed += 1
        results += f'<tr class="{result.lower()}">\n'
        results += f"<td>{html.escape(item["label"])}</td>"
        results += f'<td class="center">{html.escape(result)}</td>'
        results += f"<td>{html.escape(remarks[i].GetValue().strip())}</td>"
        results += "</tr>\n"
    results += "</table>"

    template_values["result"] = "FAILED"
    if n_passed == len(ITEMS):
        template_values["result"] = "PASSED"
    ratio = 100 * n_passed / len(ITEMS)
    template_values["result_message"] = f"{n_passed} of {len(ITEMS)} passed ({ratio:.1f}%)"
    template_values["checklist_results"] = results
    template_values["result_class"] = template_values["result"].lower()

    template_filename = os.path.join(os.path.dirname(view_checklist.__file__),
                                     "html_report_template.html")
    report_filename = os.path.join(os.path.dirname(tests.__file__), "test_reports",
                                   f"{timestamp}_release_checklist.html")
    with open(template_filename, "r", encoding="utf-8") as fp:
        template = fp.read()
    with open(report_filename, "w", encoding="utf-8") as fp:
        fp.write(Template(template).substitute(template_values))

    if open_in_browser:
        webbrowser.open(report_filename)

    wx.GetTopLevelWindows()[0].Close()


def show_checklist():
    app = wx.App(redirect=False)
    ViewCheckList(ITEMS, AppData.VERSION, check_callback).Show()
    app.MainLoop()


if __name__ == "__main__":

    show_checklist()
