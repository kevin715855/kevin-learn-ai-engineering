# Vercel Deployment Guide

This project is configured for deployment on Vercel.

## Prerequisites

- A Vercel account
- The Vercel CLI installed (`npm i -g vercel`)
- Access to the repository

## Deployment Steps

1. **Install dependencies** (if not already done):
   ```bash
   npm install
   ```

2. **Build the project locally** (optional, to verify):
   ```bash
   npm run build
   ```
   The output will be in `frontend/dist`.

3. **Deploy to Vercel**:
   ```bash
   vercel
   ```
   Follow the prompts to configure your project.

4. **Alternatively, connect your Git repository**:
   - Push the code to a Git repository (GitHub, GitLab, or Bitbucket)
   - Import the project on Vercel dashboard
   - Vercel will automatically detect the `vercel.json` configuration and deploy

## Configuration Details

The `vercel.json` file configures Vercel to:
- Use the `@vercel/static-build` builder for the frontend
- Set the output directory to `frontend/dist`
- Rewrite all routes to `index.html` for client-side routing (React Router)

## Environment Variables

If your application requires environment variables, configure them in the Vercel dashboard under Settings > Environment Variables.

## Troubleshooting

- **Build failures**: Ensure that the frontend directory contains a valid `package.json` and that the build script (`npm run build`) works locally.
- **404 errors**: Verify that the rewrite rule is correctly configured to serve `index.html` for all routes.
- **Missing assets**: Check that the build output is correctly placed in `frontend/dist` and that static assets are referenced correctly in the HTML.

## Further Reading

- [Vercel Documentation](https://vercel.com/docs)
- [Deploying a Vite app on Vercel](https://vercel.com/guides/deploying-vite-with-vercel)