// if (document.getElementById('name').value == "" )  {
//     alert('※ニックネームを入力してください！');
// }

// if (document.getElementById('password').value == "" )  {
//     alert('※パスワードを入力してください！');
// }

// function check(){
//   var a=document.reg.password.value;
//   if(a==""){
//     alert('※入力してください！');
//   }
// }

function check(){
  var a=document.reg.name.value;
  var b=document.reg.password.value;
  if(a==""){
    alert('※ニックネームを入力してください！')
    return false;
  }else if(!a.match(/\S/g)){
    alert('※ニックネームを入力してください！')
    return false;
  }else if(b==""){
    alert('※パスワードを入力してください！')
    return false;
    }else if(!b.match(/\S/g)){
      alert('※パスワードを入力してください！')
      return false;
    }
  }