function likePost(id){

    console.log("inside like function", id)
    fetch(`/post/like/${id}`)
            .then( response => response.json() )
            .then( data =>  {
        var element = document.querySelector(`.post${id}`) 
        num = element.textContent
        console.log(element.textContent)
        num1 = "hello"
        console.log("hello num is " + num )
        newNum = Number(num) + 1
        console.log(newNum)
        element.textContent = newNum
        buttonSwitcher(id)

        
    } )
    }

function buttonSwitcher(id){
    var likeButton = document.querySelector(`.like${id}`)
    var unlikeButton =  document.querySelector(`.unlike${id}`)

    likeButton.style.display = 'none';
    unlikeButton.style.display = 'block'
}

function unlikePost(id){

    console.log("inside unlike function", id)
    fetch(`/post/unlike/${id}`)
            .then( response => response.json() )
            .then( data =>  {
        var element = document.querySelector(`.post${id}`) 
        num = element.textContent
        newNum = Number(num) - 1
        element.textContent = newNum
        buttonSwitcher2(id)
    } )
    }

function buttonSwitcher2(id){
    var likeButton = document.querySelector(`.like${id}`)
    var unlikeButton =  document.querySelector(`.unlike${id}`)

    likeButton.style.display = 'block';
    unlikeButton.style.display = 'none'
}




function likeReply(id){
    console.log("inside reply like function", id)
    fetch(`/reply/like/${id}`)
            .then( response => response.json() )
            .then( data => {
        var element = document.querySelector(`.reply${id}`) 
        num = element.textContent
        newNum = Number(num) + 1
        element.textContent = newNum
        buttonSwitcher(id)


        
    } )
    }



function unlikeReply(id){

    console.log("inside unlike function", id)
    fetch(`/reply/unlike/${id}`)
            .then( response => response.json() )
            .then( data =>  {
        var element = document.querySelector(`.reply${id}`) 
        num = element.textContent
        newNum = Number(num) - 1
        element.textContent = newNum
        buttonSwitcher2(id)

    } )
    }


function follow(id){

    fetch(`/user/follow/${id}`)
            .then( response => response.json() )
            .then( data => {
        followSwitcher(id)
    } )
}


function unfollow(id){

    fetch(`/user/unfollow/${id}`)
            .then( response => response.json() )
            .then( data => {
        followSwitcher2(id)
    } )
}

function followSwitcher(id){
    console.log("*****follow switcher******")
    console.log(id)
    var followButton = document.querySelector(`#follow${id}`)
    var unfollowButton =  document.querySelector(`#unfollow${id}`)

    followButton.style.display = 'none';
    unfollowButton.style.display = 'block'
}

function followSwitcher2(id){
    var followButton = document.querySelector(`#follow${id}`)
    var unfollowButton =  document.querySelector(`#unfollow${id}`)

    followButton.style.display = 'block';
    unfollowButton.style.display = 'none';
}