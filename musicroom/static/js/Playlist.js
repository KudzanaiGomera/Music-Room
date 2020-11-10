function openNav() {
    document.getElementById("myNav").style.display = "block";
  }

  function openNav3() {
    document.getElementById("myNav5").setAttribute('class','');
  }
  function closeNav3() {
    document.getElementById("myNav5").setAttribute('class','overlay');
  }  

  function closeNav() {
    document.getElementById("myNav").style.display = "none";
  }

  function openNav2(value) {
    document.getElementById("myNav2").style.display = "block";
  }
  function closeNav2() {
    document.getElementById("myNav2").style.display = "none";
  }
  function get_name(input_name)
  {
     document.getElementById('user_input').value=input_name
  }
  function add_private_user()
  {
    var add_private_user=[]
    add_private_user.push(document.getElementById('user_input').value)
    return add_private_user
  }

  function get_user_array(json_user)
  {
    user_names=[]
    $.each(json_user, function(i,item){
      user_names.push(json_user[i].fields.username)
    });
    return user_names
  }
  function get_user(json_user)
  {
    var user_names = get_user_array(json_user)
    document.getElementById('user_input').value=''
    user = document.querySelector('#user_input')
    user_list = document.querySelector('.user_list')
    user.addEventListener('keyup', function() {
      var input = user.value
      user_list.innerHTML=''
      var search_results=user_names.filter(function(found_user){
        return found_user.toLowerCase().startsWith(input.toLowerCase());
      })
      if (search_results.length == 0)
        search_results = ["No user found"]
      search_results.forEach(function(results){
      var create_div = document.createElement('div')
      create_div.innerHTML= results;
      create_div.addEventListener('click', function(){
        if (results != "No user found")
            get_name(results)
      })
      user_list.appendChild(create_div)})
      if (input ==='')
        user_list.innerHTML=''
    })
    
  }
  // get_dezeer_playlist(JSON.parse('{{ hold2 | safe }}'))
  function get_dezeer_playlist(json_playlist)
  {
    var hold = json_playlist
    playlist_deezer_array=[]
    for (k=0;k<hold['data'].length;k++){
      playlist_deezer_array.push(hold['data'][k]['title'])}
      return playlist_deezer_array
  }
  // function create_playlist()
  // {
    // 
  // }
