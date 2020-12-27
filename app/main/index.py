# file name : index.py
# pwd : /project_name/app/main/index.py
from flask import session, Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as current_app
import datetime

from app.module import dbModule

main = Blueprint('main', __name__, url_prefix='/')


@main.route('/', methods=['GET'])
def index():
    db_class= dbModule.Database()

    sql = "SELECT * FROM movie"

    db_class.execute(sql)
    movielist= db_class.cursor.fetchall()

    return render_template('/main/index.html',movielist=movielist)

#회원가입
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=='GET':
        return render_template('/main/register.html')
    else:
        db_class= dbModule.Database()

        customerid=request.form['customerid']
        lastname=request.form['lastname']
        firstname=request.form['firstname']
        address=request.form['address']
        city=request.form['city']
        state=request.form['state']
        zipcode=request.form['zipcode']
        telephone=request.form['telephone']
        accountnum=request.form['accountnum']
        accounttype=request.form['accounttype']
        email=request.form['email']
        creditcard=request.form['creditcard']
        createdate=datetime.datetime.now().strftime("%Y-%m-%d")
        sql = "INSERT INTO movie.customer(customer_id, Lname, Fname, address, city, state, zip_code, telephone, account_num, account_type,customer_email,credit_card,acc_create_date) \
                    VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%s', '%s', '%s')"% (customerid,lastname,firstname,address,city,state,zipcode,telephone,int(accountnum),accounttype,email,creditcard,createdate)

        db_class.execute(sql)
        db_class.commit()

        return redirect('/')

@main.route('/customerMovie', methods=['GET'])
def customerMovie():
    if 'user' in session:
        db_class= dbModule.Database()

        sql = "select m.movie_name ordered_movie, co.rating from customer_order co, customer c, movie m \
                where co.customer_id=c.customer_id and c.customer_id='%s' \
                    and co.movie_id=m.movie_id and co.return_date is null order by m.movie_name asc"%session['user']

        db_class.execute(sql)
        result= db_class.cursor.fetchall()

        return render_template('/main/index.html',orderlist=result)
    else:
        return'''
            <script> alert("로그인 후 이용 가능합니다"); 
            location.href="/"
            </script> 
            '''


@main.route('/customerQueue', methods=['GET'])
def customerQueue():
    if 'user' in session:
        db_class= dbModule.Database()

        sql = "select m.movie_name from customer c, movie m, movie_queue mq \
                where c.customer_id='%s' and c.customer_id=mq.customer_id and \
                    c.account_num=mq.account_num and m.movie_id=mq.movie_id order by m.movie_name asc"%session['user']

        db_class.execute(sql)
        result= db_class.cursor.fetchall()

        return render_template('/main/index.html',customerqueue=result)
    else:
        return'''
            <script> alert("로그인 후 이용 가능합니다"); 
            location.href="/"
            </script> 
            '''

@main.route('/customerAccount', methods=['GET'])
def customerAccount():
    if 'user' in session:
        db_class= dbModule.Database()

        sql = "select account_type, credit_card, acc_create_date \
                from customer c where c.customer_id='%s' order by customer_id asc"%session['user']

        db_class.execute(sql)
        result= db_class.cursor.fetchall()

        return render_template('/main/index.html',accountdata=result)
    else:
        return'''
            <script> alert("로그인 후 이용 가능합니다"); 
            location.href="/"
            </script> 
            '''

@main.route('/availableTypeMovie', methods=['GET','POST'])
def availableTypeMovie():
    if request.method == 'GET':
        return render_template("/main/findbytype.html")
    else:
        movie_type=request.form['movietype']
        db_class= dbModule.Database()

        sql = "select movie_name from movie m where movie_type='%s'"%movie_type

        db_class.execute(sql)
        result= db_class.cursor.fetchall()

        return render_template('/main/index.html',findmovietype=result,type=movie_type)

@main.route('/findMoviebyword', methods=['GET','POST'])
def findMoviebyword():
    if request.method == 'GET':
        return render_template('/main/findbyword.html')
    else:
        if request.form['word']=='':
            return'''
                <script> alert("단어를 입력해 주세요"); 
                location.href="/"
                </script> 
                '''
        else:
            db_class= dbModule.Database()
            words=request.form['word'].split(',')

            result=[]

            if(len(words)==1):
                sql = "select movie_name from movie where movie_name like '%%"+words[0]+"%%'"

                db_class.execute(sql)
                result = db_class.cursor.fetchall()
            else:
                sql = "select movie_name from movie where movie_name like '%%"+words[0]+"%%' and movie_name like '%%"+words[1]+"%%'"

                db_class.execute(sql)
                result = db_class.cursor.fetchall()

            return render_template('/main/index.html',findmovieword=result, words=words)

@main.route('/findMoviebyActor', methods=['GET','POST'])
def findMoviebyActor():
    if request.method == 'GET':
        return render_template('/main/findbyactor.html')
    else:
        if request.form['actor']=='':
            return'''
                <script> alert("배우 이름을 입력해 주세요"); 
                location.href="/"
                </script> 
                '''
        else:
            db_class= dbModule.Database()
            actors=request.form['actor'].split(',')

            result=[]
            if len(actors)==1:
                sql = "select m.movie_name, a.actor_name from movie m, actor_movie_table amt, actor a \
                        where m.movie_id=amt.movie_id and amt.actor_id=a.actor_id and a.actor_name='%s'"%actors[0]
            else:
                sql = "select distinct m.movie_name, a1.actor_name, a2.actor_name from movie m, actor_movie_table amt, actor a1, actor a2 where m.movie_id=amt.movie_id and \
                        m.movie_id in(select amt1.movie_id from actor_movie_table amt1 where a1.actor_id=amt1.actor_id and a1.actor_name='%s') and \
                            m.movie_id in(select amt2.movie_id from actor_movie_table amt2 where a2.actor_id=amt2.actor_id and a2.actor_name='%s')"%(actors[0],actors[1])

            db_class.execute(sql)
            result = db_class.cursor.fetchall()

            return render_template('/main/index.html',findmovieactor=result,actors=actors)

@main.route('/findBestsellerMovie', methods=['GET'])
def findBestsellerMovie():
    db_class= dbModule.Database()

    sql = "select movie_name, number_of_copy from movie where number_of_copy > 4"

    db_class.execute(sql)
    result= db_class.cursor.fetchall()

    return render_template('/main/index.html',bestsellingmovies=result)

@main.route('/suggestMovies', methods=['GET'])
def suggestMovies():
    if 'user' in session:
        db_class= dbModule.Database()

        sql = "create view find_type as select m.movie_type, count(*) from customer_order co, movie m\
                where co.customer_id='%s' and co.movie_id=m.movie_id group by movie_type order by count(*) desc, m.movie_type asc"%session['user']
        db_class.execute(sql)

        sql = "select m.movie_name, m.movie_type \
                from movie m where m.movie_type=(select movie_type from find_type limit 1) and\
                 m.movie_id not in(select co.movie_id from customer_order co where co.customer_id='%s')"%session['user']

        db_class.execute(sql)
        result= db_class.cursor.fetchall()

        sql = "drop view find_type"
        db_class.execute(sql)
        db_class.commit()

        return render_template('/main/index.html',recmovie=result)
    else:
        return'''
            <script> alert("로그인 후 이용 가능합니다"); 
            location.href="/"
            </script> 
            '''

@main.route('/rateMovie', methods=['POST'])
def rateMovie():
    db_class= dbModule.Database()

    sql = "select m.movie_name, m.movie_id from movie m, customer_order co, customer c \
            where c.customer_id='%s' and c.customer_id=co.customer_id and c.account_num=co.account_num and co.movie_id=m.movie_id"%session['user']
    
    db_class.execute(sql)
    ordered_movie= db_class.cursor.fetchall()

    for movie in ordered_movie:
        if request.form['moviename'] in movie.values():
            ordered_movie_id=list(movie.values())[1]

    sql = 'UPDATE movie.customer_order SET Rating = %d WHERE movie_id=%d'%(int(request.form['point']),ordered_movie_id)
    db_class.execute(sql)
    db_class.commit()
    
    sql= "SELECT * FROM customer_order"
    db_class.execute(sql)
    result= db_class.cursor.fetchall()

    return redirect('/customerMovie')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/main/login.html')
    else:
        customerid = request.form['customerid']
        db_class= dbModule.Database()
        sql = "select customer_id from customer where customer_id='%s'"%customerid
        db_class.execute(sql)
        result= db_class.cursor.fetchall()

        if len(result)!=0:
            session['user'] = result[0]['customer_id']
            return '''
                    <script> alert("{}님 로그인 성공"); 
                    location.href="/"
                     </script> 
                     '''.format(result[0]['customer_id'])
        else:
            return'''
                <script> alert("등록되지 않은 사용자입니다"); 
                location.href="/"
                </script> 
                '''

@main.route('/logout')
def logout():
    user=session['user']
    session.pop('user', None)
    return '''
        <script> alert("{}님 로그아웃 완료"); 
        location.href="/"
        </script> 
        '''.format(user)
