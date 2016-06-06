<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- 上述3个meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->
    <title>选择检查指标</title>

    <!-- Bootstrap -->
    <link href="/bootstrap/css/bootstrap.min.css" rel="stylesheet">
    <link href="/select2/css/select2.min.css" rel="stylesheet">
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="/bootstrap/js/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="/bootstrap/js/bootstrap.min.js"></script>
    <script src="/select2/js/select2.min.js"></script>

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
        <a href="#" class="btn btn-info">星德科研数据平台</a>
    </div>
 
    <div class="row" style="margin-top:30px">
     <!--div class="col-md-6 col-md-offset-3"-->
     <label id='projectid' style='visibility:hidden'>{{projectid}}</label>
     <div class="col-md-8">
        <div class="col-md-6">
          <div class="row">
            <span>
                候选指标
                <select id='selector' class="form-control" multiple="multiple"> </select>
            </span>
          </div>
         <div class="row">
            <span>
            自定义指标
                <input id ="textbox" type="text" class="form-control" placeholder="自定义指标">
            </span>
          </div>
        </div>
        <div class="col-md-1" style="margin-top:45px">
            <button id='transfer'>=></button>
        </div>

        <div class="col-md-5">
            <span>
                已选定的指标
                <ul id="selected" class="list-group">
                    <li class='list-group-item'></li>
                </ul>
            </span>
        </div>
    </div>
    </div><!--row-->
    <div class="row" style="margin-top:30px">
        <div class="col-md-1">
            <button id="submit" class="btn btn-primary" style="border-radius:0" type="submit">下一步</button>
        </div>
    </div>
    </div><!--container-->
	<script type="text/javascript">
        //候选指标数据来源
        var indicators;
        $.ajax({
            url:'getIndicatorList',
            data: JSON.stringify(""),
            async : false,
            type:'POST',
            contentType: "application/json",
            dataType:'json',
            success: function(data) {
                if (data.msg == "ok") {
                    indicators = data.value;
                }
            },
            error: function(data) {
                alert('页面出错');
            },
        });
        var data = new Array();
        for (i in indicators) {
            data.push({id:i, text:indicators[i]});
        }
		
		$("#selector").select2({data:data});

        var selected = {}
        length = $("#selected").children()["length"];
        index = 0;
        $("#transfer").click(function() {
            data = $("#selector").select2('data');
            for (d in data) {
                if (!selected[data[d].text]) {
                    //$("#selected").append("<li class='list-group-item'>" + data[d].text + "</li>");
                    if (index < length) {
                        $("#selected li").eq(index).text(data[d].text);
                    } else {
                        $("#selected").append("<li class='list-group-item'>" + data[d].text + "</li>");
                    }
                    selected[data[d].text] = 1;
                    index++;
                }
            }
            textbox = $("#textbox").val().trim()
            if(textbox != "") {
                if (!selected[textbox]) {
                    if (index < length) {
                        $("#selected li").eq(index).text(textbox);
                    } else {
                        $("#selected").append("<li class='list-group-item'>" + textbox + "</li>");
                    }
                    selected[textbox] = 1;
                    index++;
                }
            }
        });
        $("#submit").click(function() {
            selectLength = $("#selected").children()["length"];
            values = new Array();
            for (i=0; i < selectLength; i++) {
                text = $("#selected li").eq(i).text();
                if (text != "") {
                    values.push(text);
                }
            }
            reqMap = {};
            projectid = $('#projectid').text();
            reqMap['projectid'] = projectid;
            reqMap['indicator'] = values;
            $.ajax({
                url:'ajaxSelectIndicator',
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
            location.href = 'newSearch?projectid=' + projectid;

        });
	</script>

  </body>
</html>
