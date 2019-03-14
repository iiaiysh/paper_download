try:
    with open('ICLR2018/Poster/Improving the Improved Training of Wasserstein GANs: A Consistency Term and Its Dual Effect.pdf') as f:
        s = f.read()
        print('read', len(s), 'bytes.')
except Exception as x:
    if x.errno == errno.ENOENT:
        print('- does not exist')
    elif x.errno == errno.EACCES:
        print( '- cannot be read')
    else:
        print('- some other error')