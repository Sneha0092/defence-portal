from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'defence-portal-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///defence.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ── MODELS ──────────────────────────────────────────────

class User(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String(100), nullable=False)
    email     = db.Column(db.String(120), unique=True, nullable=False)
    password  = db.Column(db.String(200), nullable=False)
    created   = db.Column(db.DateTime, default=datetime.utcnow)
    bookmarks = db.relationship('Bookmark', backref='user', lazy=True)
    queries   = db.relationship('Query', backref='user', lazy=True)

class Bookmark(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    force      = db.Column(db.String(20))
    entry_name = db.Column(db.String(100))
    entry_tag  = db.Column(db.String(50))
    saved_at   = db.Column(db.DateTime, default=datetime.utcnow)

class Query(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    user_id   = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    name      = db.Column(db.String(100))
    email     = db.Column(db.String(120))
    message   = db.Column(db.Text)
    submitted = db.Column(db.DateTime, default=datetime.utcnow)

class EligibilityResult(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    age     = db.Column(db.Integer)
    gender  = db.Column(db.String(10))
    edu     = db.Column(db.String(50))
    stream  = db.Column(db.String(50))
    height  = db.Column(db.Integer)
    results = db.Column(db.Text)
    checked = db.Column(db.DateTime, default=datetime.utcnow)

class FitnessLog(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    force       = db.Column(db.String(20))
    run_time    = db.Column(db.Float)
    pushups     = db.Column(db.Integer)
    situps      = db.Column(db.Integer)
    height      = db.Column(db.Integer)
    weight      = db.Column(db.Float)
    run_pass    = db.Column(db.Boolean)
    pushup_pass = db.Column(db.Boolean)
    situp_pass  = db.Column(db.Boolean)
    bmi_pass    = db.Column(db.Boolean)
    overall     = db.Column(db.Boolean)
    logged_at   = db.Column(db.DateTime, default=datetime.utcnow)

# ── ENTRY DATA ───────────────────────────────────────────

ENTRIES = [
    {"id":"nda","name":"NDA – National Defence Academy","force":"Army / Navy / Air Force","tag":"After 12th","age_min":16.5,"age_max":19.5,"gender":["male","female"],"edu":["12th"],"stream":["pcm","any"],"height_min":157,"desc":"Most prestigious entry via UPSC. Covers all three forces. Women eligible since SC ruling 2021.","note":"Women's NDA entry is being implemented in phases. Verify at upsc.gov.in","official":"https://upsc.gov.in"},
    {"id":"tes","name":"TES – Technical Entry Scheme (Army)","force":"Army","tag":"After 12th","age_min":16.5,"age_max":19.5,"gender":["male"],"edu":["12th"],"stream":["pcm"],"height_min":157,"desc":"For PCM students with 70%+. 5-year B.Tech program at CME/MCTE/MCEME. No written exam.","note":"Currently male only. Verify at joinindianarmy.nic.in","official":"https://joinindianarmy.nic.in"},
    {"id":"cds_ima","name":"CDS – IMA Entry (Permanent Commission)","force":"Army","tag":"Graduate","age_min":19,"age_max":24,"gender":["male"],"edu":["graduate","engineering"],"stream":["any","pcm"],"height_min":157,"desc":"UPSC CDS biannual exam. Permanent Commission at IMA Dehradun. 18-month training.","note":"Male only for IMA. Women apply for OTA via CDS. Verify at upsc.gov.in","official":"https://upsc.gov.in"},
    {"id":"ota","name":"OTA – Short Service Commission (Army)","force":"Army","tag":"Graduate","age_min":19,"age_max":25,"gender":["male","female"],"edu":["graduate","engineering"],"stream":["any"],"height_min":152,"desc":"SSC at OTA Chennai for men and women. 49-week training. 10+4 year commission.","note":"Women: height min 152cm. Verify at joinindianarmy.nic.in","official":"https://joinindianarmy.nic.in"},
    {"id":"jag","name":"JAG – Judge Advocate General (Army)","force":"Army","tag":"Professional","age_min":21,"age_max":27,"gender":["male","female"],"edu":["law"],"stream":["any"],"height_min":148,"desc":"Legal branch of Indian Army. LLB with 55%+ or LLM required. 14-year SSC.","note":"Bar Council enrollment required. Verify at joinindianarmy.nic.in","official":"https://joinindianarmy.nic.in"},
    {"id":"ssc_tech","name":"SSC Tech – Army (Men & Women)","force":"Army","tag":"Graduate","age_min":20,"age_max":27,"gender":["male","female"],"edu":["engineering"],"stream":["pcm"],"height_min":152,"desc":"SSC for engineering graduates in technical branches — Engineers, Signals, EME. No written exam.","note":"BE/B.Tech required in specific disciplines. Verify at joinindianarmy.nic.in","official":"https://joinindianarmy.nic.in"},
    {"id":"soldier_gd","name":"Soldier General Duty (Army)","force":"Army","tag":"10th Pass","age_min":17.5,"age_max":21,"gender":["male"],"edu":["10th","12th"],"stream":["any"],"height_min":160,"desc":"Rally-based recruitment. Largest vacancies in Indian Army. Physical, medical, written exam.","note":"Currently male only. Verify at joinindianarmy.nic.in","official":"https://joinindianarmy.nic.in"},
    {"id":"soldier_clerk","name":"Soldier Clerk / SKT (Army)","force":"Army","tag":"12th Pass","age_min":17.5,"age_max":23,"gender":["male"],"edu":["12th"],"stream":["any"],"height_min":162,"desc":"Army clerk and store keeper technical entry. 12th with 60% aggregate required.","note":"Min 60% in 12th mandatory. Verify at joinindianarmy.nic.in","official":"https://joinindianarmy.nic.in"},
    {"id":"navy_btech","name":"10+2 B.Tech Cadet Entry (Navy)","force":"Navy","tag":"After 12th","age_min":17,"age_max":19,"gender":["male"],"edu":["12th"],"stream":["pcm"],"height_min":157,"desc":"4-year B.Tech at Naval Academy Ezhimala. Direct Permanent Commission on completion.","note":"PCM 70%+ required. Currently male only. Verify at joinindiannavy.gov.in","official":"https://joinindiannavy.gov.in"},
    {"id":"inet","name":"INET – Indian Naval Entrance Test","force":"Navy","tag":"Graduate","age_min":19,"age_max":25,"gender":["male","female"],"edu":["graduate","engineering"],"stream":["any","pcm"],"height_min":152,"desc":"Navy's biannual entrance test. Executive, Technical, Education, Naval Architect branches.","note":"Women eligible for Education, Law, Logistics. Height: Male 157cm, Female 152cm.","official":"https://joinindiannavy.gov.in"},
    {"id":"navy_ssc_women","name":"Navy SSC – Women Entry","force":"Navy","tag":"Graduate","age_min":19,"age_max":25,"gender":["female"],"edu":["graduate","engineering"],"stream":["any"],"height_min":152,"desc":"SSC for women in Education, Logistics, Law, Naval Architecture. 10+4 year commission.","note":"Specific degree required per branch. Verify at joinindiannavy.gov.in","official":"https://joinindiannavy.gov.in"},
    {"id":"sailor_aa","name":"Sailor – Artificer Apprentice (Navy)","force":"Navy","tag":"After 12th","age_min":17,"age_max":20,"gender":["male"],"edu":["12th"],"stream":["pcm"],"height_min":157,"desc":"Technical sailor entry. PCM 60%+ in 12th. Training at INS Chilka.","note":"Currently male only. Verify at joinindiannavy.gov.in","official":"https://joinindiannavy.gov.in"},
    {"id":"sailor_ssr","name":"Sailor – Senior Secondary Recruit (Navy)","force":"Navy","tag":"After 12th","age_min":17,"age_max":20,"gender":["male"],"edu":["12th"],"stream":["any"],"height_min":157,"desc":"General sailor entry after 12th any stream. Multiple roles: seamanship, communication.","note":"Currently male only. Verify at joinindiannavy.gov.in","official":"https://joinindiannavy.gov.in"},
    {"id":"sailor_mr","name":"Sailor – Matric Recruit (Navy)","force":"Navy","tag":"10th Pass","age_min":17,"age_max":20,"gender":["male"],"edu":["10th","12th"],"stream":["any"],"height_min":157,"desc":"Entry after 10th for cook, steward, and hygienist roles in Indian Navy.","note":"Currently male only. Verify at joinindiannavy.gov.in","official":"https://joinindiannavy.gov.in"},
    {"id":"afcat_flying","name":"AFCAT – Flying Branch (IAF)","force":"Air Force","tag":"Graduate","age_min":20,"age_max":24,"gender":["male","female"],"edu":["graduate","engineering"],"stream":["pcm","any"],"height_min":162,"desc":"Flying Branch via AFCAT. Men: Fighter/Transport/Helicopter. Women: Transport and Helicopter only.","note":"PABT test compulsory. Vision 6/6 unaided required. Verify at careerindianairforce.cdac.in","official":"https://careerindianairforce.cdac.in"},
    {"id":"afcat_gd_tech","name":"AFCAT – Ground Duty Technical (IAF)","force":"Air Force","tag":"Graduate","age_min":20,"age_max":26,"gender":["male","female"],"edu":["engineering"],"stream":["pcm"],"height_min":152,"desc":"Technical Ground Duty via AFCAT. Aeronautical Engineering Electronics or Mechanical branch.","note":"BE/B.Tech in specific disciplines required. Verify at careerindianairforce.cdac.in","official":"https://careerindianairforce.cdac.in"},
    {"id":"afcat_gd_nontech","name":"AFCAT – Ground Duty Non-Technical (IAF)","force":"Air Force","tag":"Graduate","age_min":20,"age_max":25,"gender":["male","female"],"edu":["graduate","engineering"],"stream":["any"],"height_min":152,"desc":"Non-Technical Ground Duty: Admin, Logistics, Accounts, Education, Meteorology branches.","note":"Specific degree needed for Education/Meteorology. Verify at careerindianairforce.cdac.in","official":"https://careerindianairforce.cdac.in"},
    {"id":"cds_afa","name":"CDS – Air Force Academy (Flying Branch)","force":"Air Force","tag":"Graduate","age_min":19,"age_max":23,"gender":["male"],"edu":["graduate","engineering"],"stream":["pcm"],"height_min":162,"desc":"UPSC CDS for Flying Branch. Training at AFA Dundigal on PC-7 Mk-II and Hawk 132.","note":"PCM at graduation required. Vision 6/6 unaided. Currently male only. Verify at upsc.gov.in","official":"https://upsc.gov.in"},
    {"id":"airmen_x","name":"Agniveer Vayu – Group X (Technical)","force":"Air Force","tag":"After 12th","age_min":17.5,"age_max":21,"gender":["male","female"],"edu":["12th"],"stream":["pcm"],"height_min":152,"desc":"Technical Agniveer Vayu under Agnipath scheme 2022+. 4-year service. PCM 50%+ required.","note":"Agnipath scheme: 4-year tenure, 25% retained permanently. Verify at agnipathvayu.cdac.in","official":"https://agnipathvayu.cdac.in"},
    {"id":"airmen_y","name":"Agniveer Vayu – Group Y (Non-Technical)","force":"Air Force","tag":"After 12th","age_min":17.5,"age_max":21,"gender":["male","female"],"edu":["12th"],"stream":["any"],"height_min":152,"desc":"Non-Technical Agniveer Vayu. Roles: Aviation, Security, IT. 12th any stream 50%+.","note":"Agnipath scheme: 4-year tenure, 25% retained permanently. Verify at agnipathvayu.cdac.in","official":"https://agnipathvayu.cdac.in"},
    {"id":"afms","name":"AFMS – Armed Forces Medical Services","force":"Army / Navy / Air Force","tag":"Professional","age_min":21,"age_max":45,"gender":["male","female"],"edu":["graduate"],"stream":["any"],"height_min":148,"desc":"Medical, Dental, and Nursing Officers across all three forces. MBBS/BDS required.","note":"Age limit varies by specialization. Verify at afms.nic.in","official":"https://afms.nic.in"},
]

# ── FITNESS STANDARDS ────────────────────────────────────

FITNESS_STANDARDS = {
    "army": {"label":"Indian Army",    "run_max":7.5,"pushups_min":40,"situps_min":30,"bmi_min":18,"bmi_max":25,"color":"#6dbf82"},
    "navy": {"label":"Indian Navy",    "run_max":7.0,"pushups_min":35,"situps_min":25,"bmi_min":18,"bmi_max":25,"color":"#5fa8e8"},
    "air":  {"label":"Indian Air Force","run_max":6.5,"pushups_min":40,"situps_min":30,"bmi_min":18,"bmi_max":25,"color":"#7ec8fa"},
}

def evaluate_fitness(force, run_time, pushups, situps, height, weight):
    std         = FITNESS_STANDARDS[force]
    bmi         = round(weight / ((height/100)**2), 1)
    run_pass    = run_time <= std["run_max"]
    pushup_pass = pushups  >= std["pushups_min"]
    situp_pass  = situps   >= std["situps_min"]
    bmi_pass    = std["bmi_min"] <= bmi <= std["bmi_max"]
    overall     = all([run_pass, pushup_pass, situp_pass, bmi_pass])
    run_gap     = round(run_time - std["run_max"], 2) if not run_pass else 0
    pushup_gap  = std["pushups_min"] - pushups if not pushup_pass else 0
    situp_gap   = std["situps_min"]  - situps  if not situp_pass  else 0
    return {
        "std":std,"bmi":bmi,"run_pass":run_pass,"pushup_pass":pushup_pass,
        "situp_pass":situp_pass,"bmi_pass":bmi_pass,"overall":overall,
        "run_time":run_time,"pushups":pushups,"situps":situps,
        "height":height,"weight":weight,
        "run_gap":run_gap,"pushup_gap":pushup_gap,"situp_gap":situp_gap,
    }

# ── ELIGIBILITY LOGIC ────────────────────────────────────

def check_eligibility(age, gender, edu, stream, height):
    matched = []
    edu_hierarchy = {
        '10th':        ['10th'],
        '12th':        ['10th','12th'],
        'graduate':    ['10th','12th','graduate'],
        'engineering': ['10th','12th','graduate','engineering'],
        'law':         ['10th','12th','graduate','law'],
    }
    eligible_edu = edu_hierarchy.get(edu, [edu])
    for e in ENTRIES:
        if not (e['age_min'] <= age <= e['age_max']): continue
        if gender not in e['gender']: continue
        if not any(d in eligible_edu for d in e['edu']): continue
        if 'any' not in e['stream'] and stream not in e['stream']: continue
        if height < e['height_min']: continue
        matched.append(e)
    return matched

# ── ROUTES ───────────────────────────────────────────────

@app.route('/')
def index():
    user      = None
    bookmarks = []
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user is None:
            session.clear()  # stale session after DB reset
        else:
            bookmarks = [b.entry_name for b in Bookmark.query.filter_by(user_id=user.id).all()]
    return render_template('index.html', user=user, bookmarks=bookmarks)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name     = request.form['name'].strip()
        email    = request.form['email'].strip().lower()
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please login.', 'error')
            return redirect(url_for('register'))
        user = User(name=name, email=email, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        session['user_id']   = user.id
        session['user_name'] = user.name
        flash(f'Welcome, {name}! You are now registered.', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', user=None)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email    = request.form['email'].strip().lower()
        password = request.form['password']
        user     = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id']   = user.id
            session['user_name'] = user.name
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(url_for('index'))
        flash('Invalid email or password.', 'error')
    return render_template('login.html', user=None)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/eligibility', methods=['GET','POST'])
def eligibility():
    user      = User.query.get(session['user_id']) if 'user_id' in session else None
    if 'user_id' in session and user is None: session.clear()
    bookmarks = [b.entry_name for b in Bookmark.query.filter_by(user_id=user.id).all()] if user else []
    results   = None
    form_data = {}
    if request.method == 'POST':
        age       = float(request.form['age'])
        gender    = request.form['gender']
        edu       = request.form['edu']
        stream    = request.form['stream']
        height    = int(request.form['height'])
        form_data = dict(age=age, gender=gender, edu=edu, stream=stream, height=height)
        results   = check_eligibility(age, gender, edu, stream, height)
        er = EligibilityResult(
            user_id=session.get('user_id'), age=int(age),
            gender=gender, edu=edu, stream=stream, height=height,
            results=json.dumps([r['name'] for r in results])
        )
        db.session.add(er)
        db.session.commit()
    return render_template('eligibility.html', user=user, results=results,
                           form_data=form_data, bookmarks=bookmarks)

@app.route('/contact', methods=['GET','POST'])
def contact():
    user = User.query.get(session['user_id']) if 'user_id' in session else None
    if request.method == 'POST':
        q = Query(
            user_id=session.get('user_id'),
            name=request.form['name'].strip(),
            email=request.form['email'].strip(),
            message=request.form['message'].strip()
        )
        db.session.add(q)
        db.session.commit()
        flash('Your query has been submitted!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', user=user)

@app.route('/fitness', methods=['GET','POST'])
def fitness():
    user      = User.query.get(session['user_id']) if 'user_id' in session else None
    if 'user_id' in session and user is None: session.clear()
    result    = None
    form_data = {}
    history   = []
    if request.method == 'POST':
        force    = request.form.get('force', 'army')
        run_time = float(request.form['run_time'])
        pushups  = int(request.form['pushups'])
        situps   = int(request.form['situps'])
        height   = int(request.form['height'])
        weight   = float(request.form['weight'])
        form_data = dict(force=force, run_time=run_time, pushups=pushups,
                         situps=situps, height=height, weight=weight)
        result = evaluate_fitness(force, run_time, pushups, situps, height, weight)
        if user:
            log = FitnessLog(
                user_id=user.id, force=force,
                run_time=run_time, pushups=pushups, situps=situps,
                height=height, weight=weight,
                run_pass=result['run_pass'], pushup_pass=result['pushup_pass'],
                situp_pass=result['situp_pass'], bmi_pass=result['bmi_pass'],
                overall=result['overall']
            )
            db.session.add(log)
            db.session.commit()
    if user:
        history = FitnessLog.query.filter_by(user_id=user.id)\
            .order_by(FitnessLog.logged_at.desc()).limit(10).all()
    return render_template('fitness.html', user=user, result=result,
                           form_data=form_data, history=history,
                           standards=FITNESS_STANDARDS)

@app.route('/fitness/delete/<int:log_id>', methods=['POST'])
def delete_fitness_log(log_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    log = FitnessLog.query.get_or_404(log_id)
    if log.user_id == session['user_id']:
        db.session.delete(log)
        db.session.commit()
    return redirect(url_for('fitness'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login to view your dashboard.', 'error')
        return redirect(url_for('login'))
    user      = User.query.get(session['user_id'])
    bookmarks = Bookmark.query.filter_by(user_id=user.id).order_by(Bookmark.saved_at.desc()).all()
    queries   = Query.query.filter_by(user_id=user.id).order_by(Query.submitted.desc()).all()
    from sqlalchemy import desc
    checks = EligibilityResult.query.filter_by(user_id=user.id)\
        .order_by(desc(EligibilityResult.checked)).limit(5).all()
    for c in checks:
        c.result_list = json.loads(c.results) if c.results else []
    return render_template('dashboard.html', user=user, bookmarks=bookmarks,
                           queries=queries, checks=checks)

@app.route('/bookmark', methods=['POST'])
def bookmark():
    if 'user_id' not in session:
        return jsonify({'status':'error','msg':'Login required'}), 401
    data       = request.get_json()
    user_id    = session['user_id']
    entry_name = data.get('entry_name')
    existing   = Bookmark.query.filter_by(user_id=user_id, entry_name=entry_name).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        return jsonify({'status':'removed'})
    bm = Bookmark(user_id=user_id, force=data.get('force'),
                  entry_name=entry_name, entry_tag=data.get('entry_tag'))
    db.session.add(bm)
    db.session.commit()
    return jsonify({'status':'saved'})

@app.route('/bookmark/remove/<int:bm_id>', methods=['POST'])
def remove_bookmark(bm_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    bm = Bookmark.query.get_or_404(bm_id)
    if bm.user_id == session['user_id']:
        db.session.delete(bm)
        db.session.commit()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)