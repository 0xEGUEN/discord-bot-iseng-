#!/usr/bin/env node

/**
 * Environment Check Script
 * Verify Python, Node.js, dan dependencies
 */

import { spawn } from 'child_process';
import { existsSync } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

dotenv.config();

const log = {
  info: (msg) => console.log(`\x1b[36m[INFO]\x1b[0m ${msg}`),
  success: (msg) => console.log(`\x1b[32m[✓]\x1b[0m ${msg}`),
  error: (msg) => console.log(`\x1b[31m[✗]\x1b[0m ${msg}`),
  warning: (msg) => console.log(`\x1b[33m[!]\x1b[0m ${msg}`),
};

async function checkSystem() {
  console.log('\n\x1b[35m' + '='.repeat(60) + '\x1b[0m');
  console.log('\x1b[35m' + '    ENVIRONMENT CHECK' + '\x1b[0m');
  console.log('\x1b[35m' + '='.repeat(60) + '\x1b[0m\n');

  let issues = [];

  // Check Node.js
  log.info('Checking Node.js...');
  const nodeVersion = process.version;
  log.success(`Node.js: ${nodeVersion}`);

  // Check npm
  await new Promise((resolve) => {
    const npm = spawn('npm', ['-v'], { stdio: 'pipe', shell: true });
    let version = '';
    npm.stdout.on('data', (data) => {
      version += data.toString();
    });
    npm.on('close', () => {
      log.success(`npm: v${version.trim()}`);
      resolve();
    });
  });

  // Check Python
  log.info('Checking Python...');
  await new Promise((resolve) => {
    const python = spawn('python', ['--version'], { stdio: 'pipe', shell: true });
    let version = '';
    python.stdout.on('data', (data) => {
      version += data.toString();
    });
    python.stderr.on('data', (data) => {
      version += data.toString();
    });
    python.on('close', (code) => {
      if (code === 0) {
        log.success(`Python: ${version.trim()}`);
      } else {
        log.error('Python: Not installed');
        issues.push('Python is not installed');
      }
      resolve();
    });
  });

  // Check .env
  log.info('Checking .env file...');
  const envPath = path.join(__dirname, '.env');
  if (existsSync(envPath)) {
    log.success('.env file exists');
    const token = process.env.DISCORD_TOKEN;
    if (token && token.length > 0) {
      log.success('DISCORD_TOKEN is set');
    } else {
      log.error('DISCORD_TOKEN is not set');
      issues.push('DISCORD_TOKEN is missing in .env');
    }
  } else {
    log.error('.env file not found');
    issues.push('.env file is missing - create from .env.example');
  }

  // Check requirements.txt
  log.info('Checking requirements.txt...');
  const reqPath = path.join(__dirname, 'requirements.txt');
  if (existsSync(reqPath)) {
    log.success('requirements.txt exists');
  } else {
    log.error('requirements.txt not found');
    issues.push('requirements.txt is missing');
  }

  // Check bot.py
  log.info('Checking bot.py...');
  const botPath = path.join(__dirname, 'bot.py');
  if (existsSync(botPath)) {
    log.success('bot.py exists');
  } else {
    log.error('bot.py not found');
    issues.push('bot.py is missing');
  }

  // Summary
  console.log('\n\x1b[35m' + '='.repeat(60) + '\x1b[0m');
  if (issues.length === 0) {
    console.log('\x1b[32m✓ All checks passed! Ready to run:\x1b[0m');
    console.log('\x1b[32m  npm start\x1b[0m\n');
  } else {
    console.log('\x1b[31m✗ Found issues:\x1b[0m');
    issues.forEach((issue) => console.log(`  • ${issue}`));
    console.log();
  }
  console.log('\x1b[35m' + '='.repeat(60) + '\x1b[0m\n');
}

checkSystem();
