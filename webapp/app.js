var express = require('express');
var PythonShell = require('python-shell');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var exec = require('child_process').exec;
var routes = require('./routes/index');
var users = require('./routes/users');
var results1;
var msg;
var app = express();
var name;
var password;
var ip;
// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

// uncomment after placing your favicon in /public
//app.use(favicon(__dirname + '/public/favicon.ico'));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', routes);
app.use('/users', users);
app.post('/add',function(req,res,next){
  name = req.body.user;
  password = req.body.pswd;
  ip = req.body.ip;
  var options = {
  mode: 'json',
  pythonOptions: ['-u'],
  scriptPath: '/home/hassaan/',
  args: [name, password, ip]
  };
  PythonShell.run('get_vm_list.py',options, function (err, results){
      if (err) throw err;
      console.log('results: %j', results);
	  results1 = results
    vmlist = results1;
    params={
    "vmlist": vmlist};
     res.render('index.jade', params, function(err, html) {
         res.send(200, html);
     });
  });

/*var child;

child = exec('/home/hassaan/devstack/./unstack.sh',
  function (error, stdout, stderr) {
    console.log('stdout: ' + stdout);
    console.log('stderr: ' + stderr);
    if (error !== null) {
      console.log('exec error: ' + error);
    }
});
setTimeout(hello, 20000);*/
  
});
app.post('/migrate',function(req,res,next){
  var options = {
  mode: 'json',
  pythonOptions: ['-u'],
  scriptPath: '/home/hassaan/',
  args: [name, password, ip]
};
  PythonShell.run('automate_v2.py',options, function (err, results){
      if (err) throw err;
      console.log('results: %j', results);
      msg = "DONE!"
      params={
      "msg": msg};
      res.render('index.jade', params, function(err, html) {
         res.send(200, html);
     });
  });
});
/*function hello(){
  var child;
  child = exec('xterm -e "/home/hassaan/devstack/./rejoin-stack.sh; bash"',
    function (error, stdout, stderr) {
      console.log('stdout: ' + stdout);
      console.log('stderr: ' + stderr);
      if (error !== null) {
        console.log('exec error: ' + error);
    }
  });
} */
// catch 404 and forward to error handler
app.use(function(req, res, next) {
    var err = new Error('Not Found');
    err.status = 404;
    next(err);
});

// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
    app.use(function(err, req, res, next) {
        res.status(err.status || 500);
        res.render('error', {
            message: err.message,
            error: err
        });
    });
}

// production error handler
// no stacktraces leaked to user
app.use(function(err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
        message: err.message,
        error: {}
    });
});


module.exports = app;
