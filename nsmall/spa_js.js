	
var pageIdx    		= 1;   //page번호
var listId 			= 1;   //TAB_ID
var initBtnYn  		= "";

var isClick = false;

/* 더보기 버튼 클릭시 */
$('#moreBtn').on('click', function(){
    pageIdx++;
    getThemeTempPrdtLiat('72001', '1259564', listId, pageIdx);
});

/* 3대 매장 탭 상품 정보를 가져온다 (몰ID, 매장ID, TAB_ID, page번호)*/
function getThemeTempPrdtLiat(pCatalogId, pCatgroupIdChild, pListId, pPage) {

    if(!isClick) {
        isClick = true;
        $.ajax({
                type : "post"
            , url : "TvThemePrdtList?storeId=13001&langId=-9"
            , data : { catalogId : pCatalogId, catgroupIdChild : pCatgroupIdChild, listId : pListId, page : pPage }
            , dataType : "html" //"xml", "html", "script", "json"
            , contentType : "application/x-www-form-urlencoded; charset=UTF-8"
            , success : function(data) {
                
                if(pPage == 1) {
                    $("#tabPrdtList").html(data);
                } else {
                    $("#tabPrdtList").append(data);
                }	
                
                isClick = false;
                }
            , error: function(data, status, err) {
                console.log("error forward : "+data);
                alert('통신이 실패했습니다.');
                isClick = false;
                }
        });	
    } else {
        alert('처리 중 입니다.');
    }
    return;
}	


/* 더보기 버튼 노출 여부를 셋팅한다. (자식페이지 호출) */
function setMoreBtn(moreYn) {
    initBtnYn = moreYn;
    if(moreYn == 'N') {
        $('#moreBtn').addClass('hide');
    } else {
        $('#moreBtn').removeClass('hide');
    }	
}




/* TAB 메뉴 클릭시 */
$("a[id^='themeTempCat']").on('click', function(){
    
    pageIdx = 1;
    listId = $(this).attr('list_id');

    setEspotCookie($(this).attr('espot_id'), $(this).attr('content_id'));

    $("a[id^='themeTempCat']").removeClass("active");
    $(this).addClass("active");	

    var winTop = $(window).scrollTop();
    if(winTop > $('#deal-lst').offset().top) {
        $(window).scrollTop($('#deal-lst').offset().top);
    }
    tabScroll();	
    
    getThemeTempPrdtLiat('72001', '1259564', listId, pageIdx);
});	



/* */
function tabScroll() {

    var tabCnt = '4';
    if(tabCnt > 1){
        if ($(window).scrollTop() > $('#deal-lst').offset().top) {			
            $('#theme_tab_info').css({position:'fixed',top:0,zIndex:500,margin:0});
            $('#theme_tab_info').css('background-color', '#ffffff'); 
        } else {
            $('#theme_tab_info').removeAttr('style'); 
        }
    }
}

$(window).scroll(tabScroll);

/* 초기 한번만 실행 */
function initBtn() {
    if(initBtnYn == 'N') {
        $('#moreBtn').addClass('hide');
    } else {
        $('#moreBtn').removeClass('hide');
    }	
}
initBtn();	

// 페이지 이동 
function movePage( pid ,num ){
    if(pid == '#qna'){
        $('#pageId').val(num);
        GetQnaView(); //Q&A
    }
    else if(pid == '#review'){
        getCustomerReview(num); //공산품 상품평 리스트
    }
    else if(pid == '#Foodreview'){
        getCustomerReviewList(num);//식품 상품평 리스트
    }
    else if(pid == '#photo_review'){
        photoGetReview(num,'N');//사진 상품평 리스트
    }
    else if(pid == '#other_review'){
        GetOtherReviewList(num,'N');//다른 상품평 리스트
    }
}	