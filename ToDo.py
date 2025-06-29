import json
import argparse
from pathlib import Path

i:int = 1

FILE = Path('todo_tasks.json')

def GetArgs():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--add', type=str, help='Add a task')
    group.add_argument('--done', type=int, help='Completed task by index')
    group.add_argument('--remove', type=int, help='Remove a task at index')
    group.add_argument('--list', action='store_true', help='List all tasks')
    args = parser.parse_args()
    return args
    

def get_tasks() -> list:
    tasks:list = []
    
    if FILE.exists():
        with open(FILE, 'r') as f:
            try:
                tasks = json.load(f)
            except json.JSONDecodeError:
                print("Cannot Decode!")
    
    return tasks

def set_tasks(tasks:list):
    
    with open(FILE, 'w') as f:
        json.dump(tasks, f, indent=1)
                

def add_task(task:str):
    
    tasks = get_tasks()
    
    data = {
            "id":len(tasks) + 1, 
            "task":task, 
            "done":False
            }
    
    tasks.append(data)
     
    set_tasks(tasks)
        

def mark_done(id:int):
    
    flag = False
    tasks = get_tasks()
    
    for task in tasks:
        if task["id"] == id:
            task["done"] = True
            flag = True
        
    if flag:
        set_tasks(tasks)
        print("Done!")
    else:
        print("Fuck you")

def list_tasks():
    tasks = get_tasks()
    print("Your To-Do List")
    for task in tasks:
        done = '[x]' if task['done'] else '[ ]'
        print(f'{done} {task["id"]}. {task["task"]}')        
        
def clear_tasks():
    tasks = []
    set_tasks(tasks)
    
def remove_task(id:int):
    flag = False
    tasks = get_tasks()
    for task in tasks:
        if task['id'] == id:
            tasks.remove(task)
            flag = True
            
    if flag:
        for i ,task in enumerate(tasks, start=1):
            task['id'] = i
        set_tasks(tasks)
        print("Done")
        
    else:
        print("task with id not found")        
    

if __name__ == '__main__':
    args = GetArgs()
    if args.add:
        add_task(args.add)
    if args.remove:
        remove_task(args.remove)
    if args.done:
        mark_done(args.done)
    if args.list:
        list_tasks()
    