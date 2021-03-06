#rand F G H


import torch
import matplotlib.pyplot as plt
import random
import numpy as np
import torch.distributions.normal as normal

if __name__ == '__main__':

    S0=True     # WHEN S0=0 IS TRUE
    n=20        # length of X0
    expnumb=50  # expr numb
    group=20   # group number

    ########################################
    X0ba=torch.tensor(5.1)
    P0=torch.tensor(0.3)
    Q=torch.tensor(0.2)
    R=torch.tensor(0.1)
    # F,G,H=torch.randint(0,10,(3,n,n)).float()
    F,G,H=torch.rand(3,n,n)

    # print(torch.rand(3,n))
    # print(torch.randint(0,50,(3,n,n)))
    # F=torch.tensor([0.5464, 0.2123, 0.1930, 0.0870, 0.3876, 0.6583, 0.1053, 0.5737, 0.9286,
    #         0.3518, 0.6305, 0.5236, 0.8067, 0.6535, 0.3618, 0.2815, 0.6609, 0.6908,
    #         0.2468, 0.1061])
    # G=torch.tensor([0.1683, 0.8149, 0.2375, 0.8456, 0.0398, 0.9628, 0.2617, 0.7820, 0.4705,
    #         0.2530, 0.1102, 0.0219, 0.0353, 0.0261, 0.5870, 0.5469, 0.5830, 0.6510,
    #         0.9131, 0.6140])
    # H=torch.tensor([0.9101, 0.9938, 0.0841, 0.6890, 0.8772, 0.5248, 0.4473, 0.3421, 0.2198,
    #         0.2132, 0.3518, 0.4510, 0.1598, 0.9063, 0.1012, 0.6515, 0.6380, 0.0984,
    #         0.1173, 0.1590])
    
    ########################################
    nX0=normal.Normal(torch.tensor([X0ba]), torch.tensor([P0]))
    if S0:
        nWk=normal.Normal(torch.tensor([0.0]), torch.tensor([Q]))
        nVk=normal.Normal(torch.tensor([0.0]), torch.tensor([R]))
    else:
        pass
    ########################################
    #start
    X=torch.zeros(expnumb,group,n,n)
    Z=torch.zeros(expnumb,group,n,n)
    Xyuce=torch.zeros(expnumb,group,n,n)
    Zyuce=torch.zeros(expnumb,group,n,n)
    # Xkk=torch.zeros(expnumb,group,n,n)
    # Pkk=torch.zeros(expnumb,group,n,n)
    result=torch.zeros(expnumb,n,n)
    resultPkkjy=torch.zeros(expnumb,n,n)
    montecarlo=torch.zeros(expnumb)
    for i in range(expnumb):

        Xzero=nX0.sample(sample_shape=torch.Size([n])).reshape(-1)
        Xzero_yuce=X0ba

        for j in range(group):

            Wk=nWk.sample(sample_shape=torch.Size([n])).reshape(-1)
            Vk=nVk.sample(sample_shape=torch.Size([n])).reshape(-1)

            if j==0:

                X[i,j]=F*Xzero+G*Wk             # X1 by X0
                Xyuce[i,j]=F*Xzero_yuce+G*Wk    # X1 by X0

                # measurement update, X00 and P00 (need Z0 by X0)
                Xkk=Xzero_yuce+P0*H*torch.inverse(torch.transpose(H, 0, 1)*P0*H+R)*(torch.transpose(H, 0, 1)*Xzero_yuce+Vk-torch.transpose(H, 0, 1)*Xzero_yuce)
                Pkk=P0-P0*H*torch.inverse(torch.transpose(H, 0, 1)*P0*H+R)*torch.transpose(H, 0, 1)*P0

            else:
                
                X[i,j]=F*X[i,j-1]+G*Wk                               # X2 by X1
                Xyuce[i,j]=F*Xyuce[i,j-1]+G*Wk                       # X2 by X1
                Zyuce[i,j]=torch.transpose(H, 0, 1)*Xyuce[i,j-1]+Vk  # Z1 by X1

                # time update
                Xyuce_temp=F*Xkk
                Pyuce_temp=F*Pkk*torch.transpose(F, 0, 1)+G*Q*torch.transpose(G, 0, 1)

                # measurement update X11 and P11 (need Z1)
                Xkk=Xyuce_temp+Pyuce_temp*H*torch.inverse(torch.transpose(H, 0, 1)*Pyuce_temp*H+R)*(Zyuce[i,j]-torch.transpose(H, 0, 1)*Xyuce_temp)
                Pkk=Pyuce_temp-Pyuce_temp*H*torch.inverse(torch.transpose(H, 0, 1)*Pyuce_temp*H+R)*torch.transpose(H, 0, 1)*Pyuce_temp
           
        # print(Pkk)
        # DI I CI SHIYAN
        result[i]=(X[i,-1]-F*Xkk)*torch.transpose((X[i,-1]-F*Xkk),0,1)
        resultPkkjy[i]=F*Pkk*torch.transpose(F, 0, 1)+G*Q*torch.transpose(G, 0, 1)
        montecarlo[i]=torch.dist(torch.mean(result[:i+1],0),resultPkkjy[i],p=1)/torch.dist(resultPkkjy[i],torch.zeros(n,n),p=1)
    
    # for i in range(len(resultPkkjy)):
    #     print(torch.dist(resultPkkjy[i],resultPkkjy[i-1],p=2))
    print(montecarlo[-1])
    print(montecarlo)
        
        
        # print(torch.mean(X[i,j]-Xkk))




        
