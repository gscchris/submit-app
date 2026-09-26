from flask import Flask, request, render_template_string, redirect, url_for, session
import requests
import os
import secrets

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

PASSWORD = os.environ.get('FORM_PASSWORD', 'Coffee123!')
N8N_WEBHOOK = os.environ.get('N8N_WEBHOOK_URL', '')
DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN', '')
DISCORD_CHANNEL_ID = os.environ.get('DISCORD_CHANNEL_ID', '1553401627673763870')

LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Submit to Agent 86</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #e0e0e0;
        }
        .container {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 40px;
            width: 100%;
            max-width: 440px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        h1 {
            font-size: 24px;
            margin-bottom: 8px;
            color: #fff;
        }
        p.sub {
            color: #a0a0b0;
            margin-bottom: 24px;
            font-size: 14px;
        }
        label {
            display: block;
            font-size: 13px;
            font-weight: 600;
            color: #b0b0c0;
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        input, textarea {
            width: 100%;
            padding: 12px 14px;
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 8px;
            background: rgba(255,255,255,0.05);
            color: #e0e0e0;
            font-size: 15px;
            margin-bottom: 18px;
            transition: border 0.2s;
        }
        input:focus, textarea:focus {
            outline: none;
            border-color: #6c63ff;
        }
        textarea {
            min-height: 120px;
            resize: vertical;
        }
        button {
            width: 100%;
            padding: 12px;
            background: #6c63ff;
            color: #fff;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
        }
        button:hover { background: #5a52e0; }
        .error {
            background: rgba(255,60,60,0.15);
            border: 1px solid rgba(255,60,60,0.3);
            color: #ff6b6b;
            padding: 10px 14px;
            border-radius: 8px;
            margin-bottom: 16px;
            font-size: 14px;
        }
        .hidden { display: none; }
        .badge {
            text-align: center;
            font-size: 12px;
            color: #606070;
            margin-top: 16px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 Restricted Access</h1>
        <p class="sub">Enter the password to access the submission form.</p>
        {% if error %}<div class="error">{{ error }}</div>{% endif %}
        <form method="POST" action="{{ url_for('login') }}">
            <label for="password">Password</label>
            <input type="password" id="password" name="password" placeholder="Enter password..." autofocus>
            <button type="submit">Unlock</button>
        </form>
        <div class="badge">Agent 86 • Secure Channel</div>
    </div>
</body>
</html>
'''

FORM_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Submit to Agent 86</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #e0e0e0;
        }
        .container {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 40px;
            width: 100%;
            max-width: 520px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        h1 {
            font-size: 22px;
            margin-bottom: 6px;
            color: #fff;
        }
        p.sub {
            color: #a0a0b0;
            margin-bottom: 24px;
            font-size: 14px;
        }
        label {
            display: block;
            font-size: 13px;
            font-weight: 600;
            color: #b0b0c0;
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        textarea {
            width: 100%;
            padding: 12px 14px;
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 8px;
            background: rgba(255,255,255,0.05);
            color: #e0e0e0;
            font-size: 15px;
            margin-bottom: 18px;
            min-height: 160px;
            resize: vertical;
            transition: border 0.2s;
        }
        textarea:focus {
            outline: none;
            border-color: #6c63ff;
        }
        button {
            width: 100%;
            padding: 12px;
            background: #6c63ff;
            color: #fff;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
        }
        button:hover { background: #5a52e0; }
        .badge {
            text-align: center;
            font-size: 12px;
            color: #606070;
            margin-top: 16px;
        }
        .success {
            text-align: center;
            padding: 30px;
        }
        .success h2 { color: #4ade80; margin-bottom: 8px; }
        .success p { color: #a0a0b0; }
    </style>
</head>
<body>
    <div class="container">
        {% if submitted %}
            <div class="success">
                <h2>✅ Submission Received</h2>
                <p>Agent 86 has been notified. Thank you.</p>
                <p style="margin-top: 20px;"><a href="{{ url_for('form') }}" style="color: #6c63ff;">Submit another</a></p>
            </div>
        {% else %}
            <h1>📝 Submit Intelligence</h1>
            <p class="sub">Send information directly to Agent 86's secure channel.</p>
            <form method="POST" action="{{ url_for('submit') }}">
                <label for="message">Your Message</label>
                <textarea id="message" name="message" placeholder="Type your message here..." autofocus>{{ message or '' }}</textarea>
                <button type="submit">Send</button>
            </form>
            <div class="badge">Agent 86 • Encrypted Transmission</div>
        {% endif %}
    </div>
</body>
</html>
'''


@app.route('/')
def form():
    if 'authenticated' in session:
        return render_template_string(FORM_TEMPLATE, submitted=False)
    return render_template_string(LOGIN_TEMPLATE, error=None)


@app.route('/login', methods=['POST'])
def login():
    pw = request.form.get('password', '')
    if pw == PASSWORD:
        session['authenticated'] = True
        return redirect(url_for('form'))
    return render_template_string(LOGIN_TEMPLATE, error='Invalid password. Access denied.')


@app.route('/submit', methods=['POST'])
def submit():
    if 'authenticated' not in session:
        return redirect(url_for('form'))

    message = request.form.get('message', '').strip()
    if not message:
        return render_template_string(FORM_TEMPLATE, submitted=False, message='')

    # Forward to configured webhooks
    payload = {'message': message, 'source': 'submit.agent86.cloud'}

    if N8N_WEBHOOK:
        try:
            requests.post(N8N_WEBHOOK, json=payload, timeout=10)
        except Exception as e:
            print(f"Failed to send to n8n: {e}")

    # Send via Discord Bot API
    if DISCORD_BOT_TOKEN:
        try:
            discord_text = f"**📩 New submission from submit.agent86.cloud**\n```\n{message}\n```"
            if len(discord_text) > 2000:
                discord_text = discord_text[:1997] + "..."
            requests.post(
                f"https://discord.com/api/v10/channels/{DISCORD_CHANNEL_ID}/messages",
                headers={"Authorization": f"Bot {DISCORD_BOT_TOKEN}"},
                json={"content": discord_text},
                timeout=10
            )
        except Exception as e:
            print(f"Failed to send to Discord: {e}")

    return render_template_string(FORM_TEMPLATE, submitted=True)


@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('form'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))