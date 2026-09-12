
export default class API {
    url: string;
    data: Object;
    onStart: Function;
    onError: Function;
    onSuccess: Function
    
    constructor(url: string, data: Object, onStart: Function, onError: Function, onSuccess: Function) {
        this.url = url;
        this.data = data;
        this.onStart = onStart;
        this.onError = onError;
        this.onSuccess = onSuccess;
    }
    
    async post() {
        try {
            this.onStart && this.onStart()
            const res = await fetch(this.url, {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.data),
            });

            if (!res.ok) {
                throw new Error(`请求失败，状态码: ${res.status}`);
                this.onError && this.onError("-1", "post failed", `${res.status}`)
            }

            const resp: Map<string, Object> = await res.json();
            this.onSuccess && this.onSuccess(resp);
        } catch (err) {
            if (err instanceof Error) {
                this.onError && this.onError("-1", err.message, '')
            } else {
                this.onError && this.onError("-2", 'unknown error', '');
            }
        } finally {
            
        }
    }
}