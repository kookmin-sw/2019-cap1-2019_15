<<<<<<< HEAD
function cart(){
	var k = document.querySelector('p').getAttribute('data-product-id') ;
	if(confirm(k + "을(를) 장바구니에 담으시겠습니까?")){
		alert('추가되었습니다');}
 	else{
	 	alert('아니오를 누르셨습니다');
 }

function complete(){
	if(confirm("주문을 완료하시겠습니까 ?")){
	 location.href="no-sidebar.html";}
 else{
	 alert('아니오를 누르셨습니다');
 }
}
