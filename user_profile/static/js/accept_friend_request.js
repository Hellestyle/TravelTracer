var url = {
    accept_friend_request: "{{ url_for('user_profile.accept_friend_request', sender_name='_sender_name_') }}"
  };

document.querySelectorAll('.accept-button').forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();

        let username = event.target.closest('tr').querySelector('.username-data').textContent;
        console.log(username);
        
        let newUrl = url.accept_friend_request.replace('_sender_name_', username);
        console.log(newUrl);

        window.location.href = newUrl;
    });
});
