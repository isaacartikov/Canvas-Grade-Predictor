import requests
import os
from dotenv import load_dotenv
import pandas as pd
load_dotenv()


def update_grades():

    all_data_rows = []

    institution_url = os.getenv('INSTITUTION_URL')
    
    courses_url = f"{institution_url}/api/v1/courses?enrollment_type=student&enrollment_state=active&state[]=available&per_page=100"

    token = os.getenv('INSTITUTION_TOKEN')

    headers = {
            'Authorization': f'Bearer {token}'
    }

    courses_response = requests.get(courses_url, headers=headers)
    courses_response.raise_for_status()
    courses = courses_response.json()

    for course in courses:
        course_id=course.get('id')
        
        assignment_map = {}

        course_name=course.get('name', f"Unknown_Course_{course_id}")
        
        if course.get('access_restricted_by_date'):
            continue
        try:
            assignments_url = f"{institution_url}/api/v1/courses/{course_id}/assignments"
            assignments_response = requests.get(assignments_url, headers=headers)
            assignments_response.raise_for_status()
            assignments = assignments_response.json()
            print(f"Course: {course_name} (ID: {course_id}) has {len(assignments)} assignments.")
        except Exception as e:
            print(f"Error occured, skipping class. Error: {e}. Likely that the class is forbidden/ you don't have access.")
            continue
        for a in assignments:
            a_id=a['id']
            assignment_name=a['name']
            points_possible=a['points_possible']

            assignment_map[a_id] = {
                'course_name': course_name,
                'assignment_name' : assignment_name,
                'points_possible' : points_possible
            }

        submissions_response = requests.get(f"{institution_url}/api/v1/courses/{course_id}/students/submissions", headers=headers)
        submissions_response.raise_for_status()
        submissions = submissions_response.json()

        for s in submissions:
            score= s.get('score',None)
            info = assignment_map.get(s.get('assignment_id'))
            if score is not None and info and info.get('points_possible',0) > 0:
                points=s.get('score')
                points_possible=info['points_possible']
                row = {
                    'course': info['course_name'],
                    'name': info['assignment_name'],
                    'points': points,
                    'max_points': points_possible,
                    'percent' : (points/points_possible)*100
                }
                all_data_rows.append(row)

    df = pd.DataFrame(all_data_rows)
    df.to_csv("academic_data.csv", index=False)
    print("Grades updated with most recent data.")
    