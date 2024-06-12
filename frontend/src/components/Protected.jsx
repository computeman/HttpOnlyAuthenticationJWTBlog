import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Protected = () => {
    const [message, setMessage] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const fetchProtectedData = async () => {
            try {
                const response = await fetch('http://localhost:5000/protected', {
                    method: 'GET',
                    credentials: 'include',
                });

                if (response.status === 401) {
                    navigate('/login');
                } else {
                    const data = await response.json();
                    setMessage(data.message);
                }
            } catch (error) {
                navigate('/login');
            }
        };

        fetchProtectedData();
    }, [navigate]);

    return (
        <div>
            <h1>Protected Route</h1>
            <p>{message}</p>
        </div>
    );
};

export default Protected;
