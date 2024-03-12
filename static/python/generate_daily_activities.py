from openai import OpenAI
from datetime import datetime, timedelta
from tqdm import tqdm

import pyrootutils
pyrootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)

system_prompt = '''Your task is to provide detailed descriptions of Charlie's activities at specific times throughout the day, as requested. These activities could range from eating, sleeping, and playing, to other typical baby behaviors. Each report should follow a structured format to ensure clarity and consistency. For example, if asked about Charlie's activity at 8:00 AM, your response should be structured as follows: 'Date: 12/3 Tuesday, Time: 8:00 AM, Activity: Charlie is currently sleeping.'
'''

def main():
    client = OpenAI()
    
    test_save = 'test'
    save_file = 'static/txt/activities.txt'

    # with open(save_file, 'w') as f:
    #     f.write(test_save)

    activities = 'Monday:\n\n'

    sample_time = time_sampler(10)
    for date in tqdm(sample_time):
        for i in range(0, len(date), 12):
            merged_time = '\n'.join(date[i:i+12]) + '\n\n'
            response = client.chat.completions.create(
                model='gpt-4-0125-preview',
                messages=[
                    {'role': "system", "content": system_prompt},
                    {'role': "user", "content": merged_time}
                ],
                temperature=0
            )
            act = response.choices[0].message.content
            activities += act + '\n'
            print(act)

        # for time in date:
        #     merged_time += time + '\n'
        # print(merged_time)
        # response = client.chat.completions.create(
        #     model='gpt-4-0125-preview',
        #     messages=[
        #         {'role': "system", "content": system_prompt},
        #         {'role': "user", "content": merged_time}
        #     ],
        #     temperature=0
        # )
        # activities += response.choices[0].message.content + '\n'
    
    with open(save_file, 'w') as f:
        f.write(activities)

        # for time in date:
        #     response = client.chat.completions.create(
        #         model='gpt-4-0125-preview',
        #         messages=[
        #             {'role': "system", "content": system_prompt},
        #             {'role': "user", "content": time}
        #         ],
        #         temperature=0
        #     )
        #     act = response.choices[0].message.content
        #     activities += act + '\n'
        #     print(act)
        #     print("")

def time_sampler(interval):
    start_hour = 8
    end_hour = 22

    start_date = datetime(2024, 3, 4)
    date_samples = []
    time_samples = []

    for day in range(7):
        # Calculate the current date
        current_date = start_date + timedelta(days=day)
        # Loop from start_hour to end_hour with the specified interval
        for hour in range(start_hour, end_hour):
            for minute in range(0, 60, interval):
                # Check if it's time to stop (at or after 10:00 PM)
                if hour == end_hour and minute > 0:
                    break
                # Create a datetime object for the current time
                current_time = current_date.replace(hour=hour, minute=minute)
                # Format the output string
                formatted_string = f"Date: {current_time.strftime('%A')}, Time: {current_time.strftime('%I:%M %p')}".lstrip("0").replace(" 0", " ")
                # Append the formatted string to the list
                time_samples.append(formatted_string)
        date_samples.append(time_samples)
        time_samples = []

    return date_samples

    


if __name__ == '__main__':
    main()
    # time_sampler(10)