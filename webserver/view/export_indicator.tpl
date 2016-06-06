<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- 上述3个meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->
    <title>Export Indicator</title>

    <!-- Bootstrap -->
    <link href="/bootstrap/css/bootstrap.min.css" rel="stylesheet">
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="/bootstrap/js/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="/bootstrap/js/bootstrap.min.js"></script>
	<link rel="stylesheet" href="/bootstrap-table/bootstrap-table.css" type="text/css">
	<link rel="stylesheet" href="/bootstrap-table/bootstrap-editable.css" type="text/css">
	<script type="text/javascript" src="/bootstrap-table/bootstrap-table.js"></script>
	<script type="text/javascript" src="/bootstrap-table/bootstrap-editable.js"></script>
	<script type="text/javascript" src="/bootstrap-table/extensions/editable/bootstrap-table-editable.js"></script>
 


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
 
    <div class="row" style="margin-top:35px">
     <div class="col-md-8">
        <table class="table table-bordered table-striped">
            <thead>
                <tr>
                    % for field in fields:
                    <th>{{field}}</th>
                    %end
                </tr>
            </thead>
            <tbody>
                % for line in values:
                <tr>
                    % for value in line:
                    <td> {{value}}</td>
                    % end
                </tr>
                % end
            </tbody>
        </table>
     </div><!-- /.col-md-8 -->
     <div class="col-md-2">
        <a href='{{download}}'/>
        <button class="btn btn-primary">导出
        <span id='export' class="glyphicon glyphicon-floppy-save" aria-hidden="true"></span>
        </button>
        </a>
     </div>
    </div><!-- /.row --> 
    </div>

    <script>
    </script>

  </body>
</html>
