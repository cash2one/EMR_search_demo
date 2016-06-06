<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- 上述3个meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->
    <title>创建项目</title>

    <!-- Bootstrap -->
    <link href="/bootstrap/css/bootstrap.min.css" rel="stylesheet">
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="/bootstrap/js/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="/bootstrap/js/bootstrap.min.js"></script>

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="//cdn.bootcss.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="//cdn.bootcss.com/respond.js/1.4.2/respond.min.js"></script>

    <![endif]-->
  </head>
  <body>
    <div class="container">
    <div class="row">
        <a class="btn btn-info">星德科研数据平台</a>
    </div>
    <div class="row" style="margin-top:30px">
     <div class="col-md-6">
		<form class="form-horizontal" role="form" action="selectIndicator" method="GET">
		   <div class="form-group">
			  <label for="ProjectName" class="col-sm-2 control-label">项目名称</label>
			  <div class="col-sm-10">
				 <input type="text" class="form-control" name="projectname" 
					placeholder="Project Name">
			  </div>
		   </div>
		   <div class="form-group">
			  <label for="detail" class="col-sm-2 control-label">项目描述</label>
			  <div class="col-sm-10">
				 <input type="text" class="form-control" name="detail" 
					placeholder="Project Detail">
			  </div>
		   </div>
		   <div class="form-group">
			  <label for="owner" class="col-sm-2 control-label">创建者</label>
			  <div class="col-sm-10">
				 <input type="text" class="form-control" name="owner" 
					placeholder="Project Owner">
			  </div>
		   </div>
	
		   <div class="form-group">
			  <div class="col-sm-offset-2 col-sm-10">
				 <button type="submit" class="btn btn-primary" style="border-radius:0">下一步</button>
			  </div>
		   </div>
		</form>
      </div><!-- /.col-md-6 -->
    </div><!-- /.row --> 

    </div>

  </body>
</html>
