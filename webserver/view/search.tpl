<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- 上述3个meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->
    <title>Search</title>

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
      <div class="col-lg-6">
        <div class="input-group">
          <input id ="textbox" type="text" class="form-control" placeholder="{{keywords}}">
          <span class="input-group-btn">
            <button id="search" class="btn btn-default btn-block" type="submit">Go!</button>
          </span>
        </div><!-- /input-group -->
      </div><!-- /.col-lg-6 -->
    </div><!-- /.row --> 

    <!--<h1> Search Result </h1>-->

    <a> 相关结果{{results["total"]}}个</a>
    % for item in results["hits"]:
        <a href="show/{{item["_id"]}}" target="_blank">
        <dl class="text-left">
                <dt> {{item["_id"]}}</dt>
                <dd> {{item["_source"]["symp_text"]}}</dd>
        </dl>
        </a>
        
    % end

    <!--code for pagenation-->
    <%
        pageSize = 10
        pageNum = (int(results["total"]) + 9)/10
        currentPage = (pn+9)/pageSize
        currentPage = currentPage if currentPage > 1 else 1
        currentPage = currentPage if currentPage < pageNum else pageNum
        startPage = (currentPage-5) if (currentPage-5) > 1 else 1
        endPage =  startPage + 10
        endPage = endPage if endPage < pageNum else pageNum
        prePage = currentPage-1
        nextPage = currentPage+1
    %>

	<ul class="pagination">
      % if prePage < 1:
        <li><a>&laquo;</a></li>
      % else:
        <li><a href="search?keywords={{keywords}}&pn={{prePage}}">&laquo;</a></li>
      % end
      % for index in range(startPage, endPage):
        % if index == currentPage:
            <li class="active"><a>{{index}}<span class="sr-only">(current)</span></a></li>
        % else:
            <li><a href="search?keywords={{keywords}}&pn={{index*10}}">{{index}}</a></li>
        % end
      % end
      % if nextPage > pageNum:
	    <li><a>&raquo;</a></li>
      % else:
	    <li><a href="search?keywords={{keywords}}&pn={{nextPage}}">&raquo;</a></li>
      % end
	</ul>
    </div>

    <script type="text/javascript">
            $("#search").click(function() {
                if ( $("#textbox").val() == "") {
                    location.href = "#";
                } else {
                    location.href = "search?keywords=" + $("#textbox").val();

                }
            });
            $("#textbox").keyup(function(event) {
                    if (event.keyCode == 13) {
                        $("#search").trigger('click');
                    }
            });
    </script>



  </body>
</html>
