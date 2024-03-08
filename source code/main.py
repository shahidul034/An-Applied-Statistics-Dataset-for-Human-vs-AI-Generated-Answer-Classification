from flask import Flask, render_template,request,send_from_directory,send_file
import os, sys
import random
from datasets import Dataset
import hashlib
import pandas as pd
# new instance of flask
no_of_question=10
no_of_student=100
if getattr(sys, 'frozen', False):
    # we are running in a bundle, base folder in executable is sys._MEIPASS
    bundle_dir = sys._MEIPASS
    template_folder = bundle_dir + '/templates'
    static_folder = bundle_dir + '/static'
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    # we are running in a normal Python environment
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
    app = Flask(__name__)


@app.route('/')
def category():
    return render_template('category.html')


# Category page pick teacher
@app.route('/teacher_submit', methods=['POST'])
def teacher_submit():
    return render_template('teacher-login.html')


# Category page pick student
@app.route('/student_submit', methods=['POST'])
def student_submit():
    return render_template('student-login.html')

# @app.route('/student_reg_com', methods=['POST'])
# def student_reg_com():
#     if request.method=="POST":
#         username=request.form['username']
#         password=request.form['password']
#         subject=request.form['subject']
#         print(username,password,subject)
#     return render_template('student-login.html')

# student logs in
def user_verify(path,username,password):
    f=open(path,"r").read().split("\n")
    for x in f:
        xx=x.split(",")
        if xx[0]==username and xx[1]==password:
            return True
    return False

@app.route('/login', methods=['POST'])
def login():
    if request.form.get('student_login')=='student_login':
        username=request.form['username']
        password=request.form['password']
        ans=user_verify("data_student_reg.txt",username,password)
        if ans:
            random_questions=""
            return render_template('student-dashboard.html',question_list=random_questions)
        else:
            return render_template('student-reg.html')
    else:
        username=request.form['username']
        password=request.form['password']
        ans=user_verify("data_teacher_reg.txt",username,password)
        if ans:
            return render_template('teacher-dashboard.html')
        else:
            return render_template('teacher-reg.html')
    

@app.route('/category_reg', methods=['POST'])
def reg_form():
    if request.form.get('teacher')=='teacher':
        return render_template('teacher-reg.html')
    else:
        return render_template('student-reg.html')

def write_to_file(file_path, content):
    try:
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write(content+"\n")
            print(f"Successfully created and wrote to {file_path}")
        else:
            with open(file_path, 'a') as file:
                file.write(content+"\n")
            print(f"Successfully appended to {file_path}")
    except Exception as e:
        print(f"Error: {e}")
@app.route('/reg', methods=['POST','GET'])
def reg():
    if request.form.get('teacher_reg')=='teacher_reg':
        if request.method=="POST":
            username=request.form['username']
            password=request.form['password']
            subject=request.form['subject']
            file_path = 'data_teacher_reg.txt'
            write_to_file(file_path,username+","+password+","+subject)
            print(username,password,subject)
            return render_template('teacher-login.html')
    elif request.form.get('student_reg')=='student_reg':
        if request.method=="POST":
            username=request.form['username']
            password=request.form['password']
            subject=request.form['subject']
            file_path = 'data_student_reg.txt'
            write_to_file(file_path,username+","+password+","+subject)
            print(username,password,subject)
            return render_template('student-login.html')
    elif request.form.get('teacher_login')=='teacher_login':
        return render_template('teacher-login.html')
    elif request.form.get('student_login')=='student_login':
        return render_template('student-login.html')


ALLOWED_EXTENSIONS = {'xlsx'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# teacher downloads
@app.route('/download', methods=['POST'])
def download():
    if request.form.get('teacher')=='teacher':
        no_of_question=int(request.form['question'])
        no_of_student=int(request.form['student'])
        return send_from_directory('static\\files', "applied assignment question.xlsx", as_attachment=True)
    else:
        return send_from_directory('static\\files', "demo.xlsx", as_attachment=True)



def generate_short_hash(input_string, algorithm='md5'):
    if algorithm not in hashlib.algorithms_available:
        raise ValueError(f"Invalid hash algorithm '{algorithm}'")

    hasher = hashlib.new(algorithm)
    input_bytes = input_string.encode('utf-8')
    hasher.update(input_bytes)
    hash_value = hasher.hexdigest()
    return hash_value[:8] if algorithm == 'md5' else hash_value[:10]
@app.route('/upload', methods=['POST'])
def upload():
    
    if request.form.get('teacher')=='teacher':
        file = request.files['file']
        if file and allowed_file(file.filename):
            file_type = file.filename.rsplit('.', 1)[1].lower()
            return f"File type: {file_type} teacher uploaded successfully!!!"
        else:
            return "Invalid file type"
        
    elif request.form.get('file_merge')=='file_merge':
        path="static\student_files"
        data=[]
        for x in os.listdir(path):
            df=pd.read_excel(os.path.join(path,x))
            for x2 in df.values:
                data.append({
                    'id':generate_short_hash(x+str(x2[0]), algorithm='md5'),
                    'Question':x2[0],
                    'Answer':x2[1],
                    'Is_it_AI':0
                })
                data.append({
                    'id':generate_short_hash(x+str(x2[0]), algorithm='md5'),
                    'Question':x2[0],
                    'Answer':x2[2],
                    'Is_it_AI':1
                })
        
        df2 = pd.DataFrame.from_records(data)
        dataset = Dataset.from_pandas(df2)
        dataset.to_json(os.path.join("static\\files","dataset.jsonl"))
        return "Successfully uploaded!!!"

    else:
        file = request.files['file']
        if file and allowed_file(file.filename):
            file_type = file.filename.rsplit('.', 1)[1].lower()
            return f"File type: {file_type} student uploaded successfully!!!"
        else:
            return "Invalid file type"
        
def checking(ques,limit):
    import os
    df = pd.read_excel(r"static\files\applied assignment question.xlsx")
    file_path = "data//ques.txt"
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            print(f"File '{file_path}' created successfully.")
            st=""
            for x in df["Question"]:
                st+=f"{x},\n"
            file.write(st)

    ff=open(file_path,"r").split("\n")
    question_temp=df['Question']
    remove_ques=[]
    for x in ques:
        for i,x2 in enumerate(ff):
            xx=x2.split(",")
            if xx[0]==x:
                if xx[1]=="":
                    ff[i]=f"{xx[0]},1"
                else:
                    ff[i]=f"{xx[0]},{int(xx[1])+1}"
                    if int(xx[1])+1>=limit:
                        remove_ques.append(xx[0])
    f=open(file_path,"w")
    st=""
    for x in ff:
        st+=f"{x}\n"
    df2 = pd.DataFrame(columns=['Question'])

    for x in df:
        if x['Question'] not in remove_ques:
            df2 = df2.append({'Question': x['Question']}, ignore_index=True)

    f.write(st)
    df2.to_excel(r"static\files\applied assignment question.xlsx",index=False)





    
        




# generate questions
@app.route('/generate_questions', methods=['POST'])
def generate_questions():
    import pandas as pd
    df = pd.read_excel(r"static\files\applied assignment question.xlsx")
    random_questions = random.sample(df["Question"].tolist(), no_of_question)
    limit=(no_of_student*50)/no_of_question
    df2 = pd.DataFrame({"Question": random_questions,"Human":"","AI":""})
    checking(random_questions,limit)
    df2.to_excel("static\\files\\demo.xlsx", index=False)
    return render_template('student-dashboard.html', question_list=random_questions)


if __name__ == "__main__":
    app.run(debug=True)
