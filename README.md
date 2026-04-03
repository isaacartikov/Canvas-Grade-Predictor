# Canvas Grade Predictor

Standard Canvas grades reflect a culmination of your work over the semester. This leaves out momentum: what if you had great test scores in the beginning of the semester, but at the end, they diminished? The final would reflect that, making your total score lower. This tool helps you understand where you are **headed**, not where you currently are.

A predictive analytics engine for the Canvas LMS leveraging weighted linear regression and automated data pipelines. Features multi-institution support, chronological trend analysis, and custom weighted-logic for accurate academic risk assessment


## Features

**Data Filtering** ~ Filters out non-academic courses through user input and assignments depending on its group.<br>
**Momentum Based Prediction** ~ Projects grade after 5 assignments based on grade trajectory <br>
**User Customizability** ~ Weights grades based on user input through config <br>
**Dual-Institutional Compatibility** ~ Can collect Canvas data from two different institutions. <br>


## Setup
1. Create a file called ".env" and copy and paste the environment variables below into .env. Paste token/url in to variables. Institution one is required; institution two is optional. *IMPORTANT*: Don't share your token to anyone; it's private and meant solely for your own use.
2. Install dependencies: pip install -r requirements.txt
3. Edit config.py to define your syllabus weights, excluded Canvas courses, and courses utilizing standards-based grading.
4. Run update_grades (the file or the function in main) atleast once before using.
5. Run predictor.py, and results will be outputted in the console.

## Usage
To start the code, run python main.py. Run update_grades() upon installing, then call it again as desired. You do not need to run it every time.
You do not need to put in a second institution. If you don't want to, leave it blank.

```properties
INSTITUTION_ONE_TOKEN=token_one_here
INSTITUTION_ONE_URL=https://yourschool.instructure.com

INSTITUTION_TWO_TOKEN=token_two_here
INSTITUTION_TWO_URL=https://yourschool.instructure.com
```
