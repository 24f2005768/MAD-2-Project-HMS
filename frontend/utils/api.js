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
    // console.log(data)
    
    const response = await fetch(base + URL, data)
    if (response.ok) {
        return response.json()
    }

    // else {
    //     const error = response.json()
    //     // console.log(error)
    //     throw new Error(error.message)
    // }

    else {
        let errorData;
        try {
            errorData = await response.json()
        }
        catch{
            errorData = { message: `HTTP error ${response.status}` };
        }

        const error = new Error(errorData.message || "Request failed")
        error.status = response.status
        error.data = errorData

        throw error
    }
}