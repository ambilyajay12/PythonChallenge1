function showAlert()
{
var username=document.getElementById('username').value;
var first_name=document.getElementById('first_name').value;
var last_name=document.getElementById('last_name').value;
var email=document.getElementById('email').value;
var password=document.getElementById('password').value;
var confpassword=document.getElementById('confpassword').value;

if(!username || !first_name||!last_name||!email||!password||!confpassword)
{
alert('Please fill out required field');
}
else
{
    alert('Registration Successful');
}
}