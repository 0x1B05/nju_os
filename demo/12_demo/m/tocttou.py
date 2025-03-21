def main():
  sys_bwrite('/etc/passwd', ('plain', 'secret...'))
  sys_bwrite('file', ('plain', 'data...'))
  
  pid = sys_fork()
  sys_sched()
  
  if pid == 0:
    # attacker: symlink file -> /etc/passwd
    sys_bwrite('file', ('symlink', '/etc/passwd'))
  else:
    # sendmail (root): write to plain file
    filetype, contents = sys_bread('file')  # for check
    if filetype == 'plain':
      # TOCTTOU interval
      sys_sched()
      filetype, contents = sys_bread('file')  # for use
      match filetype:
        case 'symlink': filename = contents
        case 'plain': filename = 'file'
      sys_bwrite(filename, 'mail')
      sys_write(f'{filename} written')
    else:
      sys_write('rejected')

# Outputs:
# /etc/passwd written
# file written
# rejected
