class TokenService {
    static getAccessToken() {
        const accessToken = localStorage.getItem('accessToken');
        return accessToken ? accessToken : null;
    }

    static saveToken(token) {
        localStorage.setItem('accessToken', token);
    }

    static removeToken() {
        localStorage.removeItem('accessToken');
    }

    static getRefreshToken() {
        const refreshToken = localStorage.getItem('refreshToken');
        return refreshToken ? refreshToken : null;
    }

    static saveRefreshToken(refreshToken) {
        localStorage.setItem('refreshToken', refreshToken);
    }

    static removeRefreshToken() {
        localStorage.removeItem('refreshToken');
    }
}

export default TokenService;