#Excludes all courses that have atleast one line of text in the array somewhere in the course name.
EXCLUDED_COURSE_KEYWORDS = ["National Honor Society","Band","Jazz","Tri-M","Orientation","Advisory","Library"] 

## Input courses that are "standards-based" here. For example, a 2 would be a 70, a 2.5 a 80, 3 a 90, and so forth.
STANDARD_BASED_COURSE = ["French"]

#A list of weights for each assignment. Higher number means the model places more emphasis, lower means less.
weights_map = {    
        "test": 0.50,
        "exam": 0.50,
        "interpretive": 0.5,
        "presentational":0.5,
        "interpersonal":0.5,
        "quiz": 0.20,
        "homework":0.10,
        "webassign": 0.05,
        "warmup":0.05,
}