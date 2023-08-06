# Install
Install from pypi
```pip install flask-simple-captcha-k-fork```
Install from source
```python3 setup.py install```

# How to use
This package is intended to assign a unique CSRF string per each form submit per user session, without requiring any backend session tracking. First, you'll want to set a variable `CAPTCHA_CONFIG['SECRET_CAPTCHA_KEY']` in your app config to a random, complex string. Example: `CAPTCHA_CONFIG = {'SECRET_CAPTCHA_KEY':'wMmeltW4mhwidorQRli6Oijuhygtfgybunxx9VPXldz'}`

Second, add this to the top of your code.

```python
from flask_simple_captcha_k_fork import CAPTCHA


CAPTCHA = CAPTCHA(config=config.CAPTCHA_CONFIG)
app = CAPTCHA.init_app(app)
```

For each route you want captcha protected, add the following code:

```python
@app.route('/example', methods=['GET','POST'])
def example():
    if request.method == 'POST':
        c_hash = request.form.get('captcha-hash')
        c_text = request.form.get('captcha-text')
        
        if CAPTCHA.verify(c_text, c_hash):
            # Code to success captcha
            ...
        else:
            # Code to failed captcha
            ...

    if request.method == 'GET':
        captcha = CAPTCHA.create()
        return render_template('example.html', captcha=captcha)
```


In the HTML forms you want to generate a captcha: `{{ captcha_html(captcha) }}`

This will create something like this:
```html
<input type="text" name="captcha-text">
<input type="hidden" name="captcha-hash" value="1o9ig...">
```


To make a customized-size captcha, you can do:

```python
captcha = CAPTCHA.create(length=10, digits=True)
```
