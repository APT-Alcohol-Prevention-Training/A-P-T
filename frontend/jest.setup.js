// Learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom'

// Mock Next.js router
const mockPush = jest.fn()
const mockReplace = jest.fn()
const mockPrefetch = jest.fn()
const mockBack = jest.fn()

jest.mock('next/navigation', () => ({
  useRouter: jest.fn(() => ({
    push: mockPush,
    replace: mockReplace,
    prefetch: mockPrefetch,
    back: mockBack,
    pathname: '/',
    route: '/',
    asPath: '/',
    query: {},
  })),
  usePathname: jest.fn(() => '/'),
  useSearchParams: jest.fn(() => new URLSearchParams()),
  useParams: jest.fn(() => ({ role: 'ai' })),
}))

// Make router mocks available globally
global.mockPush = mockPush
global.mockReplace = mockReplace
global.mockPrefetch = mockPrefetch
global.mockBack = mockBack

// Mock Next.js Image component
jest.mock('next/image', () => ({
  __esModule: true,
  default: (props) => {
    // eslint-disable-next-line jsx-a11y/alt-text, @next/next/no-img-element
    return <img {...props} />
  },
}))

// Mock environment variables
process.env.NEXT_PUBLIC_API_URL = 'http://localhost:8080'
process.env.BACKEND_API_URL = 'http://localhost:8080'

// Mock global Headers object
global.Headers = class Headers {
  constructor(init) {
    this.headers = {}
    if (init) {
      Object.entries(init).forEach(([key, value]) => {
        this.headers[key.toLowerCase()] = value
      })
    }
  }
  
  get(name) {
    return this.headers[name.toLowerCase()]
  }
  
  set(name, value) {
    this.headers[name.toLowerCase()] = value
  }
}

// Store original Request if it exists
const OriginalRequest = global.Request

// Mock global Request object for API route tests
global.Request = class Request {
  constructor(input, init) {
    // If it's being called from NextRequest, let it handle
    if (this.constructor.name === 'NextRequest' && OriginalRequest) {
      return OriginalRequest.call(this, input, init)
    }
    
    this._url = input
    this.method = init?.method || 'GET'
    this.headers = new Headers(init?.headers || {})
    this.body = init?.body
  }
  
  get url() {
    return this._url
  }
  
  async json() {
    return JSON.parse(this.body)
  }
}

// Mock global Response object for API route tests
global.Response = class Response {
  constructor(body, init) {
    this.body = body
    this.status = init?.status || 200
    this.statusText = init?.statusText || 'OK'
    this.headers = new Headers(init?.headers || {})
  }
  
  async json() {
    return typeof this.body === 'string' ? JSON.parse(this.body) : this.body
  }
  
  async text() {
    return typeof this.body === 'string' ? this.body : JSON.stringify(this.body)
  }
  
  static json(data, init) {
    return new Response(JSON.stringify(data), {
      ...init,
      headers: {
        'Content-Type': 'application/json',
        ...(init?.headers || {})
      }
    })
  }
}

// Suppress console errors during tests (optional)
const originalError = console.error
beforeAll(() => {
  console.error = (...args) => {
    if (
      typeof args[0] === 'string' &&
      args[0].includes('Warning: ReactDOM.render')
    ) {
      return
    }
    originalError.call(console, ...args)
  }
})

afterAll(() => {
  console.error = originalError
})