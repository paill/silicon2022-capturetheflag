import type SocketIO from 'socket.io';
import isUndefined from 'lodash/isUndefined.js';
import pty from 'node-pty';
import { logger as getLogger } from '../shared/logger.js';
import { xterm } from './shared/xterm.js';
// import { envVersion } from './spawn/env.js';
// CTF - Import Crypto to generate random pid
import crypto from 'crypto';
// CTF - Import URL to get challenge name from request url
import url from 'url';

export async function spawn(
  socket: SocketIO.Socket,
  // args: string[],
): Promise<void> {
  
  // CTF - Get challenge name from URL
  const challengeName = url.parse(socket.request.headers.referer, true).query.challenge as string;
  // CTF - Generate random ID
  var cid = crypto.randomBytes(20).toString('hex');
  const logger = getLogger();
  // const version = await envVersion();
  // const cmd = version >= 9 ? ['-S', ...args] : args;
  //logger.debug('Spawning PTY', { cmd });
  // const term = pty.spawn('/usr/bin/env', cmd, xterm);
  // CTF - Generate docker terminal command
  const term = pty.spawn('/usr/bin/docker', ['run', '-it', '--rm', '--name', cid, '--pull=never', '--network=no-internet', 'registry/' + challengeName], xterm)
  const { pid } = term;
  // const address = args[0] === 'ssh' ? args[1] : 'localhost';
  logger.info('Process Started on behalf of user', { pid });
  // socket.emit('login');
  term.on('exit', (code: number) => {
    logger.info('Process exited', { code, pid });
    socket.emit('logout');
    socket
      .removeAllListeners('disconnect')
      .removeAllListeners('resize')
      .removeAllListeners('input');
      // CTF - Kill container on logout
      logger.info('Killing container')
      pty.spawn('/usr/bin/docker', ['stop', cid], {});
  });
  term.on('data', (data: string) => {
    socket.emit('data', data);
  });
  socket
    .on('resize', ({ cols, rows }) => {
      term.resize(cols, rows);
    })
    .on('input', input => {
      if (!isUndefined(term)) term.write(input);
    })
    .on('disconnect', () => {
      term.kill();
      logger.info('Process exited', { code: 0, pid });
      // CTF - Kill container on disconnect
      logger.info('Killing container');
      pty.spawn('/usr/bin/docker', ['stop', cid], {});
    });
}
