<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- 上述3个meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->
    <title>搜索</title>

    <!-- Bootstrap -->
    <link href="/bootstrap/css/bootstrap.min.css" rel="stylesheet">
    <link href="/select2/css/select2.min.css" rel="stylesheet">
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="/bootstrap/js/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="/bootstrap/js/bootstrap.min.js"></script>
    <script src="/select2/js/select2.min.js"></script>

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
      <div class="col-lg-6">
        <div class="input-group">
          % keywords = 'Search for ...' if keywords is None or len(keywords) == 0 else keywords
          <input id ="textbox" type="text" class="form-control" placeholder="{{keywords}}">
          <span class="input-group-btn">
            <button id="search" class="btn btn-default btn-block" type="submit">搜索
                <span class="glyphicon glyphicon-search" aria-hidden="true"></span>
            </button>
          </span>
        </div><!-- /input-group -->
      </div><!-- /.col-lg-6 -->
    
    </div><!-- /.row --> 

    <!-- indicator filter -->
    <div class="row">
    <div class="col-lg-3">
        <select id='selector' class="form-control" multiple="multiple"> </select>
        <ul id="filter" class="list-group">
            <!--
            % for indicator in indicatorRange:
                <li class='list-group-item' title="{{indicator}}">
                    {{indicator}}
                    <input id='low' value="{{indicatorRange[indicator][0]}}" type='text' style='width:16%;margin-left:32px;margin-right:8px'>
                    <span class='glyphicon glyphicon-minus'></span>
                    <input id='high' value="{{indicatorRange[indicator][1]}}" type='text' style='width:16%;margin-left:8px;margin-right:8px'>
                </li>
            % end
            --!>
        </ul>
    </div>
    </div>

   <!--<h1> Search Result </h1>-->
    <div class="row">
    <div class="col-lg-8">

    % if len(results) != 0:
        <a> 相关结果{{results["total"]}}个</a>
        % for item in results["hits"]:
            % if projectid is not None and len(projectid) != 0:
                <a href="editSearchResult?projectid={{projectid}}&emrid={{item["_id"]}}" target="_blank">
            % else:
                <a href="show/{{item["_id"]}}" target="_blank">
            % end
            <dl class="text-left">
                    <dt> {{item["_id"]}}</dt>
                    <dd> {{item["_source"]["symp_text"][0:256]}}...</dd>
            </dl>
            </a>
            
        % end

        <!--code for pagenation-->
        <%
            pageSize = 10
            pageNum = (int(results["total"]) + 9)/10
            currentPage = (pn+10)/pageSize
            currentPage = currentPage if currentPage > 1 else 1
            currentPage = currentPage if currentPage < pageNum else pageNum
            startPage = (currentPage-5) if (currentPage-5) > 1 else 1
            endPage =  startPage + 10
            endPage = endPage if endPage < pageNum else pageNum
            prePage = currentPage-1
            nextPage = currentPage+1
        %>

        <ul class="pagination">
          % if prePage < 1 or currentPage == 1:
            <li><a>&laquo;</a></li>
          % else:
            % newurl = url + "&pn=" + str(prePage*10 - 10)
            <!--<li><a href="search?keywords={{keywords}}&pn={{prePage*10 - 10}}">&laquo;</a></li>-->
            <li><a href="{{newurl}}">&laquo;</a></li>
          % end
          % for index in range(startPage, endPage+1):
            % if index == currentPage:
                <li class="active"><a>{{index}}<span class="sr-only">(current)</span></a></li>
            % else:
                % newurl = url + "&pn=" + str(index*10 - 10)
                <!--<li><a href="search?keywords={{keywords}}&pn={{index*10 - 10}}">{{index}}</a></li>-->
                <li><a href="{{newurl}}">{{index}}</a></li>
            % end
          % end
          % if nextPage > pageNum or currentPage == pageNum:
            <li><a>&raquo;</a></li>
          % else:
            % newurl = url + "&pn=" + str(nextPage*10 - 10)
            <!--<li><a href="search?keywords={{keywords}}&pn={{nextPage*10 - 10}}">&raquo;</a></li>-->
            <li><a href="{{newurl}}">&raquo;</a></li>
          % end
        </ul>
    % end
    </div>
    % if projectid is not None and len(projectid) != 0:
    <div id='save' class='col-lg-2 col-xs-offset-1'>
        <button class="btn btn-primary">汇总
        <span class="glyphicon glyphicon-tasks" aria-hidden="true"></span>
        </button>
    </div>
    % end
    </div>
    </div>
    <script type="text/javascript">
            //var data = [{id:0, text:'血常规'}, {id:1, text:'尿常规'}, {id:2, text:'生化'}];
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
		    $("#selector").select2({data:data, placeholder: "选择一个过滤指标", allowClear: true});

            var filterIndexMap = {};
            var filterIndex = 0;
            $("#selector").on("select2:select", function(evt) {
                selected = $(evt.target).find("option:selected").children().prevObject;
                length = selected["length"];
                for (i=0; i < length; i++) {
                    text = selected.get(i).text;
                    if (!(text in filterIndexMap)) {
                        li = "<li class='list-group-item'" + "title='" + text + "' >" + 
                            "" + text + "" +
                            "<input id='low' type='text' style='width:16%;margin-left:32px;margin-right:8px'>"+
                            "<span class='glyphicon glyphicon-minus'></span>" +
                            "<input id='high' type='text' style='width:16%;margin-left:8px;margin-right:8px'>"+
                            "</li>"
                            //"<input type='text' class='input-mini'></span>" +
                            //"<input type='text' class='col-xs-1'></li>"+
                        $("#filter").append(li);
                        filterIndexMap[text] = filterIndex;
                        filterIndex++;
                    }
                }
 
            });

            $("#selector").on("select2:unselect", function(evt) {
                /*!!!先执行了select2的删除操作,因此evt获得的selected是删除之后的状态, 求当前状态与selectText的差集*/
                selected = $(evt.target).find("option:selected").children().prevObject;
                length = selected["length"];
                subSelect = {}
                for (i=0; i < length; i++) {
                    text = selected.get(i).text;
                    subSelect[text] = 1;
                }
                var delText = ""
                for (var d in filterIndexMap) {
                    if (!(d in subSelect)) {
                        delText = d;
                    }
                }
                $("#filter li").remove("[title='" + delText + "']");
                delete filterIndexMap[delText];
 
            });
            
        	function getUrlParam(name) {
				var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
				var r = window.location.search.substr(1).match(reg);  //匹配目标参数
				if (r != null) return unescape(r[2]); return null; //返回参数值
        	} 
            $("#search").click(function() {
                filter = $("#filter");
                length = filter.children()["length"];
                params = {}
                for (i=0; i < length; i++) {
                    indicator = $("#filter li").eq(i).text();
                    low = $("#filter li").eq(i).find('#low').val();
                    high = $("#filter li").eq(i).find('#high').val();
                    if (low.length == 0 || high.length == 0) {
                        return;
                    }
                    params[indicator] = low + ":" + high;
                }

                if ( $("#textbox").val() == "") {
                    location.href = "#";
                } else {
                    //location.href = "search?keywords=" + $("#textbox").val();
					projectid = getUrlParam('projectid');
                    url = "newSearch?keywords=" + $("#textbox").val();
                    if (projectid != null) {
                        url += "&projectid=" + projectid;
                    }
                    for (p in params) {
                        url += "&" + p + "=" + params[p];
                    }
                    location.href = url;

                }
            });
            $("#textbox").keyup(function(event) {
                    if (event.keyCode == 13) {
                        $("#search").trigger('click');
                    }
            });
            $(function() {
                $(window).scroll(function() {
                    var top = $(window).scrollTop();
                    $("#save").animate({"top":top}, 10);
                });
            });
            
            $("#save").click(function() {
				projectid = getUrlParam('projectid');
                url = 'exportIndicator?projectid=' + projectid;
                location.href = url

            });
        
    </script>



  </body>
</html>
