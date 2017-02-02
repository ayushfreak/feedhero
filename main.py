from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_wtf import Form 
from wtforms import TextField,PasswordField, SubmitField,IntegerField
import feedparser
from feedfinder2 import find_feeds
import psycopg2
conn = psycopg2.connect(host="localhost",database='feedlinks', user='postgres', password='ayush1990')
c = conn.cursor()
app = Flask(__name__)
app.secret_key = 'development key'
class info(Form):
	url=TextField("URL")
	submit=SubmitField("submit")
	feed=TextField("Rss Feed")
	submit=SubmitField("submit")


@app.route('/',methods = ['GET', 'POST'])
def main():
	a=0
	form=info()
	if request.method=='POST':
		url=form.url.data	
		feed=form.feed.data	
		if(url):
			rssfeed= find_feeds(url)
		elif(feed):
			rssfeed=feed
		else:
			return render_template('main.html',form=form)
		print(rssfeed)
		t="CREATE TABLE feedinfo(sno serial,title character varying,link character varying)"
		c.execute(t)
		rss = feedparser.parse(rssfeed[0])
		for i in range(len(rss.entries)):
			c.execute("INSERT INTO feedinfo (title,link) VALUES (%s,%s)",(rss.entries[i]['title'],rss.entries[i]['link'])) 
		c.execute("SELECT * FROM feedinfo")		
		data=c.fetchall() 	
		c.execute("DROP TABLE feedinfo")		
		conn.commit()				
		return render_template('sucess.html',data=data)
	else:
		return render_template('main.html',form=form)
	
if __name__ == '__main__':
	app.run(debug=True)
