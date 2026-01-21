const base = 'http://localhost:5000/api';

export async function requestAPI(method, body = null, URL) {
    const token = localStorage.getItem('token');
    let data = {
        headers: {
            "Content-Type": "application/json",
            "Authentication-Token": token
        }, 
        method: method
    }

    if (body != null) {
        data['body'] = JSON.stringify(body)
    }
    
    const response = await fetch(base + URL, data)
    if (response.ok) {
        return response.json()
    }

    else {
        throw new Error(response.message)
    }
}