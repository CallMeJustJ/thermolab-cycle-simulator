from flask import Flask, render_template, request, jsonify
import os
app=Flask(__name__)
def diesel(p1,t1c,tmaxc,r):
    cp,cv,k,R=1.004,0.718,1.4,0.287
    t1=t1c+273.15; t3=tmaxc+273.15
    if r<=1: raise ValueError("Compression ratio must exceed 1.")
    t2=t1*r**(k-1)
    if t3<=t2: raise ValueError("Maximum temperature must exceed compression-end temperature.")
    p2=p1*r**k; rc=t3/t2
    if rc>=r: raise ValueError("Cut-off ratio must be lower than compression ratio.")
    t4=t3*(rc/r)**(k-1); qin=cp*(t3-t2); qout=cv*(t4-t1); w=qin-qout
    v1=R*t1/p1; v2=v1/r
    return dict(r=r,rc=round(rc,4),eta=round(100*w/qin,2),mep=round(w/(v1-v2),2),work=round(w,2),t4=round(t4,2))
def rankine(plow,phigh,tc,m):
    from CoolProp.CoolProp import PropsSI
    lo=plow*1e6; hi=phigh*1e6; tin=tc+273.15
    if hi<=lo: raise ValueError("Boiler pressure must exceed condenser pressure.")
    h1=PropsSI("H","P",lo,"Q",0,"Water"); v1=1/PropsSI("D","P",lo,"Q",0,"Water")
    h2=h1+v1*(hi-lo); h3=PropsSI("H","P",hi,"T",tin,"Water"); s3=PropsSI("S","P",hi,"T",tin,"Water")
    h4=PropsSI("H","P",lo,"S",s3,"Water"); wt=h3-h4; wp=h2-h1; qin=h3-h2; wn=wt-wp
    hf=PropsSI("H","P",lo,"Q",0,"Water"); hg=PropsSI("H","P",lo,"Q",1,"Water"); x=(h4-hf)/(hg-hf)
    return dict(p=phigh,eta=round(100*wn/qin,2),power=round(m*wn/1e6,3),work=round(wn/1000,3),pump=round(wp/1000,3),quality=round(x,4) if 0<=x<=1 else None)
@app.route("/")
def home(): return render_template("index.html")
@app.post("/api/diesel")
def api_diesel():
    d=request.get_json()
    try: return jsonify(results=[diesel(float(d["p"]),float(d["t1"]),float(d["tmax"]),float(r)) for r in d["ratios"]])
    except Exception as e: return jsonify(error=str(e)),400
@app.post("/api/rankine")
def api_rankine():
    d=request.get_json()
    try: return jsonify(results=[rankine(float(d["low"]),float(p),float(d["temp"]),float(d["mass"])) for p in d["pressures"]])
    except Exception as e: return jsonify(error=str(e)),400
if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.environ.get("PORT",5000)))
