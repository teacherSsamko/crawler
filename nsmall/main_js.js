
// 방송시간 체크
var lbrdEndTimeStr = '10:19';

//방송시간 체크
$(function(){
	if(lbrdEndTimeStr && lbrdEndTimeStr.length > 0) clock();
});

//방송시간 체크
var timer;
function clock() {
    var now = new Date();
    var lbrdEndTime = new Date();
    var lbrdEndTimeArray = lbrdEndTimeStr.split(":");
    lbrdEndTime.setHours(lbrdEndTimeArray[0]);
    lbrdEndTime.setMinutes(lbrdEndTimeArray[1]);
    lbrdEndTime.setSeconds(0);

    var gap = (lbrdEndTime.getTime() - now.getTime())/1000;
    var leftTime = "";

    if(gap <= 0){
        leftTime = "00:00:00";
        $("#countNum").html(leftTime);
        clearTimeout(timer);
        setTimeout("clock2()", 120000);
        return;
    }

    var hour = parseInt(gap/3600);
    var min = parseInt((gap%3600)/60);
    var sec = parseInt(gap%60);

    leftTime += ((hour < 10) ? "0":"") + hour;
    leftTime += ((min < 10) ? ":0":":") + min;
    leftTime += ((sec < 10) ? ":0":":") + sec;


    $("#countNum").html(leftTime);
    timer = setTimeout("clock()", 1000);
}

//방송시간 체크
function clock2(){
	document.location.href = "/front/tvPlusShopMainR.do";
}

//쿠키값 가져오기
function getCookie(name) {
    var cname = name + "=";
    var dc = document.cookie;
    if (dc.length > 0) {
        begin = dc.indexOf(cname);
        if (begin != -1) {
            begin += cname.length;
            end = dc.indexOf(";", begin);
            if (end == -1) end = dc.length;
            if ( "EHCustName" == name || "LAST_SECT" == name) {
                return decodeURIComponent(dc.substring(begin, end));
            }
            else {
                return unescape(dc.substring(begin, end));
            }
        }
    }
    return null;
}
    
//테그 URL
function getClickUrl(url){
	if(url == ''){
		return false;		
	}else{
		document.location.href = url;
		
	}
}

//카테고리 리스트
function getListMainItems(lastItemIndex){
	
	lastItemIndex = Number(lastItemIndex) + 1;
	
	$.ajax({
        type: "get"
        , dataType: "html"
        , url: "/front/dpl/getListMainItems.do"
        , data: { lastItemIndex : lastItemIndex}
        , success: function(data){
        	$(".moreCateItem").html('');
            $("#cateItemListIn").append(data);
        }
        , error: function(xhr, status, error) {
            //alert("시스템 오류입니다. 다시 시도해주세요.");
        }
    });
	
}

function goBuyDirect(url,slitmCd,intgItemGbcd,bsitmCd,sectId){
    if(isLogin() != 'true') {
        //보험 상품인 경우
        openLoginPopup(locationHref);
    }else{
        $("#itemInfForm input[name=slitmCd]").val(slitmCd);
        $("#itemInfForm input[name=bsitmCd]").val(bsitmCd);
        $("#itemInfForm input[name=sectId]").val(sectId);
        var input = $("<input type='hidden' name='uitmCdInf'/>");
        $(input).val("0^00001|1");
           $("#itemInfForm").append(input);
        
        $("#itemInfForm").ajaxSubmit({
            url: "/front/oda/buyDirect.do"
            , dataType: "json"
            , async:true
            , success: function(data) {
                if(!isEmpty(data.errorMessages)) {
                    var errorMessage = data.errorMessages;
                    if(errorMessage != 'noMessage') { 
                       alert(data.errorMessages.join("\n"));
                    }
                } else {
                    $("#itemInfForm").attr("action", "https://www.hyundaihmall.com/front/oda/order.do");
                    $("#itemInfForm").attr("target", "");
                    $("#itemInfForm").submit();
                }
            }
            , error: function(xhr, status, error) {
                window.location=url;
            }
        });
    }
}


