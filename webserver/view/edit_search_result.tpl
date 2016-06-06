<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- 上述3个meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->
    <title>编辑已选择指标</title>

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
 
    <div class="row" style="margin-top:35px">
     <label id='projectid' style='visibility:hidden'>{{projectid}}</label>
     <label id='emrid' style='visibility:hidden'>{{emrid}}</label>
     <div class="col-md-12">
        <!--左侧显示病例全文-->
        <div class="col-md-8">
            <iframe frameborder=0 src="show/{{emrid}}" width="100%" height="600px">
            </iframe>
        </div>
        <!--右侧显示检查指标-->
        <div class="col-md-4" style="margin-top:100px">
            <div class="row">
            <div class="panel panel-success">
                <div class="panel-heading">
                    <h3 class="panel-title">已选择的检查指标</h3>
                </div>
                <div class="panel-body">
                    <ul id="indicator" class="list-group">
                    % for k in indicator:
                        <li class="list-group-item">
                            <label>{{k}}</label>
                            <input type="text" value="{{indicator[k]}}" style="width:80%;margin-left:10px">
                        </li>
                    % end
                    </ul>
                </div>
            </div>
            </div>
            <div class="row">
               <div class="col-md-2" style="width=30px">
                    <button id="save" class="btn btn-primary"> 保存
                    <span class="glyphicon glyphicon-floppy-save" aria-hidden="true"></span>
                    </button>
                 </div>
            </div>
        </div>
     </div><!-- /.col-md-8 -->
      </div><!-- /.row --> 

    </div>
    <script type="text/javascript">
        $("#save").click(function() {
            length = $("#indicator").children().length;
            params = {};
            for (i=0; i<length; i++) {
                indicator = $("#indicator li").eq(i).find("label").text();
                value = $("#indicator li").eq(i).find("input").val();
                params[indicator] = value;
            }
            reqMap = {};
            reqMap['projectid'] = $('#projectid').text();
            reqMap['emrid'] = $('#emrid').text();
            reqMap['indicator'] = params;
            $.ajax({
                url:'ajaxEditSearchResult',
                data: JSON.stringify(reqMap),
                async : false,
                type:'POST',
                contentType: "application/json",
                dataType:'json',
                success: function(data) {
                    if (data.msg != "ok") {
                        alert(data);
                    }
                },
                error: function(data) {
                    alert('页面出错');
                },
            });
            alert("保存成功");

        });
    </script>
  </body>
</html>
