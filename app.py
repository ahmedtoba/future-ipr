from flask import Flask, render_template, request
import jinja2
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go

app = Flask(__name__)
env = jinja2.Environment()
app.jinja_env.filters['zip'] = zip
env.globals.update(zip=zip)


@app.route('/')

def index():
    result = False
    return render_template('index1.html',result=result)



@app.route('/' , methods=['GET', 'POST'])
def result():
    result = True
    if request.method == 'POST':
        Prp = float(request.form['Prp'])
        Prf = float(request.form['Prf'])
        Uop = float(request.form['Uop'])
        Uof = float(request.form['Uof'])
        Bop = float(request.form['Bop'])
        Bof = float(request.form['Bof'])
        Sop = float(request.form['Sop'])
        Sof = float(request.form['Sof'])
        krop = float(request.form['krop'])
        krof = float(request.form['krof'])
        qo = float(request.form['qo'])
        pwf = float(request.form['pwf'])
        step = int(request.form['step'])

        qomaxp = qo / (1 - .2 * (pwf/Prp) - .8 * (pwf/Prp)**2)
        Pwf = list(np.arange(Prp,-1,-1))
        qop = [round((qomaxp * (1 - .2 * (i/Prp) - .8 * (i/Prp)**2)),2) for i in Pwf]

        fPrp = krop/(Uop*Bop)
        fPrf = krof/(Uof*Bof)
        qomaxf = qomaxp * ((Prf*fPrf)/(Prp*fPrp))
        Pwff = np.arange(Prf,-1,-1)
        qof = [round((qomaxf * (1 - .2 * (i/Prf) - .8 * (i/Prf)**2)),2) for i in Pwff]

        qoft = []
        for i in Pwf :
            if i > Prf :
                qoft.append("-")
            else :
                qoft.append(round(qomaxf * (1 - .2 * (i/Prf) - .8 * (i/Prf)**2),2))


        Present = go.Scatter(x=qop, y=Pwf, name='Present IPR')
        Future = go.Scatter(x=qof, y=Pwff, name='Future IPR')

        myChart = py.plot({
                  'data': [Present, Future],
                  'layout': go.Layout(title='Present IPR V.S Future IPR curves', xaxis=dict(title='qo, STB/day'), yaxis=dict(title='Pwf, Psig'), autosize=False,width=500,height=450)
                  },output_type='div', show_link='False',include_plotlyjs='Flase',link_text="")

        tabPwf = [int(i) for i in Pwf]
        for i in tabPwf[:step+1]:
            if i % step == 0 :
                index = tabPwf.index(i)
        tabPwf = tabPwf[index::step]
        tabPwf = [round(Prp)]+tabPwf
        tabqop = qop[0]+qop[index::step]
        tabqop = np.append(tabqop , round(qomaxp))
        tabqoft = ['-'] + qoft[index::step]

        count=[]
        for i in tabPwf :
            count.append(tabPwf.index(i)+1)


        return render_template('index1.html', myChart=myChart, count=count, result=result, Bop=Bop, Bof=Bof, Pwf=tabPwf, qop=tabqop, qoft=tabqoft, Prp=Prp, Prf=Prf, Uop=Uop, Uof=Uof, Sop=Sop, Sof=Sof, krop=krop, krof=krof, pwf=pwf, qo=qo, step=step)

if __name__ == '__main__' :
    app.run(debug=True)
