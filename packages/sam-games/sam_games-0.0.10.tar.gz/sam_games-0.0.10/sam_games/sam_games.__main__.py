import random

def score():
    global dict,l
    dict={'What is the capital of Tamil Nadu':'Chennai','Who is the Indian Cricket team captain':'Rohit Sharma',
    'Who is the First Indian Boxer to win an Olympic medal':'Vijendar Sigh','Capital of India':'New Delhi',
    'Which is the worlds most populated country in the world':'China'}
    l=['What is the capital of Tamil Nadu','Who is the Indian Cricket team captain','Capital of India',
    'Which is the worlds most populated country in the world','Who is the First Indian Boxer to win an Olympic medal']
    score=0
    q=[5]
    for i in range(1,6):
        print('Question',i)
        while True:
            a=random.randint(0,4)
            if a not in q:
                q.append(a)
                break           
        print(l[a])  
        ans=input('Answer:')
        if dict[l[a]]==ans:
            score+=1
    return score

def remark(x):
    global dict2
    dict2={'0':'General Knowledge will always help you.Take it seriously','1':'Need to take interest','2':'Read more to score',
    '3':'Good','4':'Excellent','5':'Outstanding'}
    xy=str(x)
    rem=dict2[xy]
    print(rem)

ques=score()
remark(ques)

