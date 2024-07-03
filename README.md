
# *Đồ án môn học lập trình ứng dụng web*
*GV: Trần Tuấn Dũng*

## *Team 15:*
22520645 - Nguyễn Phan Hữu Khánh

22521399 - Đặng Chí Thịnh

22520724 - Trần Hoàng Tuấn Kiệt

22520678 - Nguyễn Ngọc Khoa

22521147 - Võ Văn Phúc

## *Tên đề tài:* OpenU
### *Giới thiệu ứng dụng:*
    
**OpenU** là nền tảng giúp bạn thể hiện bản thân và kết nối với cộng đồng một cách dễ dàng. Tạo blog, chia sẻ câu chuyện và quản lý không gian cá nhân của bạn một cách linh hoạt. Khám phá và tương tác với những người có cùng sở thích qua các tính năng tìm kiếm và chat tiện lợi.


### *Sơ đồ ứng dụng:*
<img src="mindmap.png" alt="drawing" width="700" height="400"/>

### *Database:*
<img src="dbmap.png" alt="drawing" width="700" height="400"/>

### *Mô tả chức năng*
- Mỗi người dùng tạo và sử dụng 1 tài khoản
- Tạo và đăng blog công khai hoặc đơn giản chỉ là viết nhật ký riêng tư
- Chỉnh sửa ảnh đại diện, thông tin cá nhân.
- Quản lý blog cá nhân: set trạng thái,xóa, xem các blog đã like
- Tính năng tìm kiếm blog và mọi người
- **Thông báo realtime**
- **Chat**

### *Công nghệ sử dụng:*

- HTML,CSS,JS đối với Front-end

- Python đối với Back-end

- SQLite cho tạo và quản lý database

- Framework: Flask

### *Package dependencies*
- Flask
- Flask-SocketIO
- Flask-Bcrypt
- Flask-Cors
- Werkzeug
- bcrypt
- uuid
- python-dotenv
- eventlet
- gunicorn

### *Trả lời các câu hỏi nhận được từ nhóm khác:
1. Sự khác biệt giữa Django và Flask:
- Django:
+ Full-stack framework: Cung cấp nhiều tính năng tích hợp sẵn như ORM (Object-Relational Mapping), hệ thống quản lý người dùng, hệ thống template, và nhiều tính năng khác.
+ Nguyên tắc DRY (Don't Repeat Yourself): Django khuyến khích việc tái sử dụng mã và giảm thiểu sự lặp lại.
+ Kiến trúc cấu trúc: Django có cấu trúc thư mục và tệp rất rõ ràng và bắt buộc.
+ Admin panel: Django có sẵn bảng điều khiển quản trị để quản lý các mô hình dữ liệu.
- Flask:
+ Microframework: Flask rất nhẹ và linh hoạt, chỉ cung cấp những gì cần thiết để bắt đầu xây dựng ứng dụng.
+ Tùy chỉnh cao: Người dùng có thể chọn các thành phần cần thiết và tích hợp chúng vào ứng dụng theo cách riêng của mình.
+ Không có cấu trúc bắt buộc: Flask không áp đặt cấu trúc thư mục cụ thể, cho phép người dùng tổ chức dự án theo cách riêng của họ.
+ Phù hợp với các ứng dụng nhỏ: Flask rất tốt cho các dự án nhỏ và các ứng dụng cần tùy chỉnh cao.

2. Flask có hỗ trợ middleware hay không:
- Flask có hỗ trợ middleware thông qua các cơ chế như before_request, after_request, và các extension. Middleware trong Flask được sử dụng để xử lý các yêu cầu HTTP trước khi chúng đến view hoặc sau khi chúng rời khỏi view.

3. Flask mạnh về độ bảo mật do Flask hay do sử dụng tài nguyên của Python:
- Flask tự bản thân không cung cấp nhiều tính năng bảo mật tích hợp như Django. Tuy nhiên, bảo mật của Flask được tăng cường nhờ vào việc sử dụng các thư viện và tài nguyên bảo mật mạnh mẽ của Python, như itsdangerous để tạo token bảo mật, Flask-Login để quản lý người dùng, và Flask-WTF để chống lại các cuộc tấn công CSRF.

4. Tại sao cần phương thức GET, bởi vì cơ bản chỉ cần POST là được:
- Phương thức GET: Được sử dụng để truy xuất dữ liệu từ máy chủ. GET yêu cầu dữ liệu từ một tài nguyên đã được xác định.
+ Ưu điểm:
Dữ liệu có thể được đánh dấu bởi URL, cho phép người dùng chia sẻ và đánh dấu các liên kết.
Được lưu trữ trong bộ nhớ cache của trình duyệt và có thể được lưu trong lịch sử trình duyệt.
Thường nhanh hơn vì không yêu cầu payload trong yêu cầu HTTP.
- Phương thức POST: Được sử dụng để gửi dữ liệu đến máy chủ để xử lý (ví dụ: nộp form).
+ Ưu điểm:
Có thể gửi dữ liệu lớn vì dữ liệu được gửi trong body của yêu cầu HTTP.
Bảo mật hơn vì dữ liệu không xuất hiện trong URL.
- Render một web trên Flask:

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

5. Làm thế nào để xử lí các form web dữ liệu từ người dùng trong Flask:
- Để xử lý dữ liệu từ form web trong Flask, bạn có thể sử dụng Flask-WTF để dễ dàng quản lý và bảo mật form.
+ Ví dụ:
  
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitButton
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

class MyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitButton('Submit')

@app.route('/form', methods=['GET', 'POST'])
def form():
    form = MyForm()
    if form.validate_on_submit():
        name = form.name.data
        return redirect(url_for('success', name=name))
    return render_template('form.html', form=form)

@app.route('/success/<name>')
def success(name):
    return f'Hello, {name}!'

if __name__ == '__main__':
    app.run(debug=True)
+ HTML template (form.html):

html
Sao chép mã
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Form Example</title>
</head>
<body>
    <form method="POST">
        {{ form.hidden_tag() }}
        {{ form.name.label }} {{ form.name }}
        {{ form.submit }}
    </form>
</body>
</html>

