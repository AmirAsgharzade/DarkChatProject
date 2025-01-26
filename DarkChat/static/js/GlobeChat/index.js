function fetchMessages() {

      
    // selecting random color 
    
    $.ajax({
        url: '/messages',
        method: 'GET',
        success: function(messages) {
            const container = $('#message-container');
            container.empty(); // Clear previous messages
            messages.forEach(function(msg) {
                const messageElement = $('<li class="list-group-item p-1"></li>');
                let username = $('<span class="username" id="what"></span>').text(msg.username+":")
                username.css('color',msg.color)
                let content = $('<span></span>').text(msg.body)
                messageElement.append(username)
                messageElement.append(content)
                
                
                container.append(messageElement);
                
            });
        },
        error: function(xhr, status, error) {
            console.error('Error fetching messages:', error);
        }
    });
}

    // Fetch messages every 5 seconds
    setInterval(fetchMessages, 500);

$('#message-form').submit(function(e){
    username = document.getElementById('Username').value
    message = document.getElementById('Message').value
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: "/send_messages",
        data: JSON.stringify({username, message}),
        contentType: "application/json;charset=utf-8",
        dataType: "json",
        success: function(data){}
    });
    document.getElementById('Message').value = '';
    
});

