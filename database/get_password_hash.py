from werkzeug.security import generate_password_hash as gph

print(gph("123456789", salt_length=16))
print(len(gph("123456789", salt_length=16)))

print(gph("123456789", salt_length=32))
print(len(gph("123456789", salt_length=32)))

#print(len('pbkdf2:sha256:260000$VbQE4vmVFufH7xPP$5b9c528d2508c47912a0820722617c96f40a33c27bc51509f69a0362c7b78432'))

