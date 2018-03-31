<script type="text/javascript" >
  window.onload=function(){
$(".a").each(function(){
    var name = $(this).attr("name");
     if(name=="led1"||name=="led4") 
    {
    this.selectedIndex=1;
    $(this).slider("refresh");
    }
  });
$('.a').on("change",function(){
  var tag = this.selectedIndex;
  var status="off";
  if(tag==1)
    status="on";
  var name = $(this).attr('name');
  var data="name="+name+"&status="+status;  
  alert(data);        
          $.ajax({
                        url:'led1',
                        type:'post',
                        data:data,
                        dataType:'json',
                        success:function(result){     
                        }
                  });
      });
};
  </script>