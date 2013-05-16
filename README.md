prams (简体中文)
=====
## 背景
PRAMS 全成为 Post Request and Approval Management System，在线单位工作申请与审批系统，我 2013 年春季学期的一个课程设计。这是一个用 Python 基于 Flask 的一个网页 APP。

这是我第一次写网页，也是第一次写网页 APP。有很多知识都是在这个程序开发的过程中学会的。只实现了后端的一些技术，由于不多那个 JS 和 HTML5，前端看起来不慎简陋（后端也就是能凑合运行而已）。

此程序上传在这里，作为我 Github 旅程的开始。

##  介绍
PRAMS 的实现的大致业务是：用户提交一个工作申请单，然后让单位里不同角色的人员协作审批。一个申请作为一个 Subject，经由不同的人按一定的流程会处在某个状态，当前的状态会决定此申请下一步会交给哪个工作人员处理。

## 具体要求 （英文）
1. sections 1 and 2 should be completed by the Head of Department, A job description。
2. The form should then be e-mailed to the relevant Human Resources Manager for the department who will complete section 3a. HR will allocate an establishment reference number and enter on to the centrally held Iog in HR before e-mailing to Management Accounts.
3. Management Accounts WiII complete section3b and return to HR.
4. HR will email the completed form to the appropriate member of the senior management team seeking approval to proceed.
5. The Director of operations & Registra/ Faculty Dean will consider the request and conform in section3c whether it is approved, declined or referred, VVhere the request is not within budget allocation or if it has implication on other area of the college, the request will be referred to the Deputy Principal for a decision on behalf of PRC。
6. The form should then be returned to HR who wiII notify the HOD and Management Accounts of the decision. HR Will update the central log and pass the form to the recruitment Team and information & systems Team for action if  appropriate. A copy of this form will be saved electronically and a copy will be kept with the job file (for recruitment) and/or on the employee’ s personaI file.

## 安装和执行
1. 安装 python27；
2. 安装 flask 库；
3. 安装 flask-sqlalchemy;
4. 安装 sqlite3，如果没有请下载该程序，放于 prams 目录下即可；
5. 直接运行 testuser.py，此文件会建立一个新的数据库（如果之前没有的话）；
6. 用 python 执行文件 prams.py;
7. 在 chrome 中 输入 http://127.0.0.1:5000/
8. There you go.

## 运行
1. 请查看 testuser.py
2. 选择职位为 ADM 或者 HOD 的用户登陆系统，密码在文件中对应的位置有标注。

暂时写到这里吧。。。
