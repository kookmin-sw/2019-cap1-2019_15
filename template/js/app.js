function cart(k){
	var x = document.getElementById("k").value
	if(confirm(x + "을(를) 장바구니에 담으시겠습니까?")){
	 location.href="http://cdmanii.tistory.com";}
 else{
	 alert('아니오를 누르셨습니다');
 }
}// x에다가 id로 전달하는거 수정하기

function complete(){
	if(confirm("주문을 완료하시겠습니까 ?")){
	 location.href="no-sidebar.html";}
 else{
	 alert('아니오를 누르셨습니다');
 }
}
