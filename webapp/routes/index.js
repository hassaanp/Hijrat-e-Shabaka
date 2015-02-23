var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res) {
  res.render('index');
});
router.get('/done', function(req, res) {
  res.render('done');
});
module.exports = router;
