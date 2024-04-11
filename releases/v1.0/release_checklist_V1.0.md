# Release checklist V1.0

Date: 2024-04-11
Result: PASSED

| Test                                             | Result | Remarks            |
|:-------------------------------------------------|:------:|:-------------------|
| All issues in GitHub fixed                       | passed |                    |
| Correct version in AppData                       | passed |                    |
| All unit tests passed on Windows                 | passed |                    |
| All unit tests passed on Ubuntu                  | failed | tests needs fixing |
| All test configuration runs passed on Windows    | passed |                    |
| All test configuration runs passed on Ubuntu     | passed |                    |
| Documentation up to date                         | passed |                    |
| Create deployment for Windows                    | passed |                    | 
| Create deployment for Ubuntu                     | passed |                    |
| Duration test passed on Windows using deployment | passed |                    |
| Duration test passed on Ubuntu using deployment  | passed |                    |
| Publish deployment on LilyTronics                | passed |                    |
| Publish deployment on GitHub                     | passed |                    |
| Set tag in git                                   | passed |                    |

[unit tests report V1.0](https://htmlpreview.github.io/?https://github.com/LilyTronics/lily-data-logger-studio-ce/blob/main/releases/v1.0/20240322_190128_TestRunner.html)

The unit tests fail in Ubuntu due to bugs in the tests itself.
Because all unit tests pass on Windows, all configurations and durations tests pass
on Windows and Ubuntu we decide to pass this release test and publish this version.
