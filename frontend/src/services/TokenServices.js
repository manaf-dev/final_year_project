class TokenService {
    static getAccessToken() {
        return localStorage.getItem('accessToken');
    }

    static saveToken(token) {
        localStorage.setItem('accessToken', token);
    }

    static removeToken() {
        localStorage.removeItem('accessToken');
    }

    static getRefreshToken() {
        return localStorage.getItem('refreshToken');
    }

    static saveRefreshToken(refreshToken) {
        localStorage.setItem('refreshToken', refreshToken);
    }

    static removeRefreshToken() {
        localStorage.removeItem('refreshToken');
    }
}

export default TokenService;