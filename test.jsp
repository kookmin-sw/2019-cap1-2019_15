<%@ page language="java" contentType="text/html; charset=EUC-KR"
    pageEncoding="EUC-KR"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">  
<html> 
<head> 
<meta charset="UTF-8"> 
<title>Kiosk</title> 
<style> 
body 
{ 
  background:purple;
} 
</style> 
<script> 
var ProductArray = new Array(); 
 
function ActAmericano(){ document.getElementById("product").value = 'Americano';} 
function ActCaramel(){ document.getElementById("product").value = 'Caramel';} 
function ActChoco(){ document.getElementById("product").value = 'Choco';} 
function ActLatte(){ document.getElementById("product").value = 'Latte';} 
function change(num) 
{ 
  var x  = document.form; 
  var y = Number(x.count.value) + num; 
  if(y < 1) y = 1; 
  x.count.value = y; 
} 
function cal(){ 
  var a = document.getElementsByName("Americano"); 
  var n = document.getElementById( document.getElementById("product").value ).getAttribute('name'); 
  var m = document.form.count.value; 
  document.getElementById('price').value=n*m; 
  return a; 
} 
function order(){ 
  var b = parseInt(document.form.price.value); 
  document.getElementById("total").value = parseInt(document.getElementById("total").value) + b; 
  ProductArray.push([document.getElementById("product").value, document.getElementById("count").value, document.getElementById("price").value]); 
} 
function reset(){ 
  document.getElementById("total").value = 1 ; 
} 
function purchase(str){ 
  location.href="screen2.html"; 
} 

function newWindow() { 
  var newWindow = window.open("", "MsgWindow", "width=200, height=100"); 
      for(var i in ProductArray){ 
        
          for (var j in ProductArray[i]){ 
              newWindow.document.write(ProductArray[i][j]+" "); 
         } 
         newWindow.document.write("<br>"); 
    } 
 } 
 </script> 
 </head> 
 <body> 
 <form name='form'> 
 <table> 
     <tr> 
     <td>Name &nbsp;<input type='text' id='product' value='' size='9'> &nbsp; 
      <td>Amount &nbsp; 
      <td><input type='text' id='count' value='' size='3'> 
      <td><p onmouseover='change(1);' onmouseout='cal();'>¡ã</p> 
      <td><p onmouseover='change(-1);' onmouseout='cal();'>¡å</p> 
      <td> &nbsp;Price &nbsp;<input type='text' id='price' value='0' size='9'> 
      <td> &nbsp;Order &nbsp;<input type='button' id='Order' onmouseover='order();' size='9' value="Look at this!"> 
      <td> &nbsp;Total &nbsp;<input type='text' id='total' value='0' size='9'> 
      <td> &nbsp;Reset &nbsp;<input type='button' id='Reset' onmouseover='reset();' size='9' value='Look at this!'> 
     <td> &nbsp;Purchase &nbsp;<input type='button' id='Purchase' onmouseover='purchase();' size='9' value='Look at this!'> 
     <td>Test <input type='button' id='test' onmouseover='test();'> </tr> 
    </table> 
 <table> 
 <tr><img src='background.png' height=30 width=30 id="Americano" name="3000" onMouseOver='setTimeout("ActAmericano()",1500);'><br> 
 <img src='background.png' height=30 width=30 id="Caramel" name="3500" onMouseOver='setTimeout("ActCaramel()",1500);'><br> 
 <img src='background.png' height=30 width=30 id="Choco" name="4000" onMouseOver='setTimeout("ActChoco()",1500);'><br> 
 <img src='background.png' height=30 width=30 id="Latte" name="4000" onMouseOver='setTimeout("ActLatte()",1500);'> 
 </tr></table> 
 <br><button type="button" onclick="newWindow()">»õÃ¢¶ç¿ì±â</button> 
 </form> 
 </body> 
 </html> 
