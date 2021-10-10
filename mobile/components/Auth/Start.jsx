import React from 'react';
import { Text, Image } from 'react-native';
import styled from 'styled-components/native';


const StartScreen = () => {
    return (
        <Group>
            <Group>
                <Image source={{ uri: "https://picsum.photos/200/300" }} />
                <Text>Welcome</Text>
            </Group>
        </Group>
    )
}


const Group = styled.View`
`;

export { StartScreen }