import requests
from dotenv import load_dotenv
from config import EXCLUDED_COURSE_KEYWORDS, STANDARD_BASED_COURSE
import pandas as pd
import os
load_dotenv()


def fetch_data(institution_url, token,all_data_rows):

    
    courses_url = f"{institution_url}/api/v1/courses?enrollment_type=student&enrollment_state=active&state[]=available&per_page=100"

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

        if any(excl.lower() in course_name.lower() for excl in EXCLUDED_COURSE_KEYWORDS):
            print(f"Skipping non-academic class {course_name}")
            continue

        groups_url = f"{institution_url}/api/v1/courses/{course_id}/assignment_groups"
        groups_response = requests.get(groups_url, headers=headers)
        groups = groups_response.json()
        zero_weight_group_ids = [g['id'] for g in groups if g.get('group_weight') == 0]

        try:
            assignments_url = f"{institution_url}/api/v1/courses/{course_id}/assignments?per_page=100"
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
            group_id= a.get('assignment_group_id')

            if group_id in zero_weight_group_ids:
                print(f"Skipping assignment {assignment_name} in zero-weight activity.")
                continue

            assignment_map[a_id] = {
                'course_name': course_name,
                'assignment_name' : assignment_name,
                'points_possible' : points_possible
            }
        submissions_url=f"{institution_url}/api/v1/courses/{course_id}/students/submissions?per_page=100"
        submissions_response = requests.get(submissions_url, headers=headers)
        submissions_response.raise_for_status()
        submissions = submissions_response.json()

        for s in submissions:
            score= s.get('score',None)
            info = assignment_map.get(s.get('assignment_id'))
            if score is not None and info and info.get('points_possible',0) > 0:
                name=info['course_name']
                points=s.get('score')
                points_possible=info['points_possible']
                percent=(points/points_possible)*100
                if any(std.lower() in name.lower() for std in STANDARD_BASED_COURSE):
                    if score==2.0:
                        percent=70
                    elif score==2.5:
                        percent=80
                    elif score==3.0:
                        percent=90
                    elif score==3.5:
                        percent=95
                    elif score==4.0:
                        percent=100
                    else:
                        percent=60
                row = {
                        'course': name,
                        'name': info['assignment_name'],
                        'points': points,
                        'max_points': points_possible,
                        'percent' : percent
                }

                all_data_rows.append(row)
    return all_data_rows


def update_grades():
    master_list=[]
    
    master_list=fetch_data(os.getenv("INSTITUTION_ONE_URL"),os.getenv("INSTITUTION_ONE_TOKEN"),master_list)

    second_url=os.getenv("INSTITUTION_TWO_URL", None)
    second_token=os.getenv("INSTITUTION_TWO_TOKEN", None)
    if  second_url and second_token:
        fetch_data(second_url,second_token,master_list)
    else:
        print("Second token/url not set, not merging two Canvas submissions.")
    pd.DataFrame(master_list).to_csv("academic_data.csv",index=False)
    print("Grades updated in academic_data.csv")

if __name__ == "__main__":
    update_grades()
    
