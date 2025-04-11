import {
  Body,
  Container,
  Head,
  Heading,
  Html,
  Img,
  Link,
  Preview,
  Text,
  Button,
  Section,
  Row,
  Column,
} from '@react-email/components';

interface PageProps {
  empresa: string;
  in18: string;
}

const main = {
  backgroundColor: '#ffffff',
};

const container = {

}

const baseURL = "https://berylliumdev.com/images";

const heading = {
  color: '#4d7af4',
  fontFamily: 'Arial, sans-serif',
}

const text = {
  verticalAlign: "middle",
  margin: "15px auto",
  font: "12px Arial, sans-serif",
}

export const BerylliumEmailEmail = ({
  empresa,
  in18,
}: PageProps) => {

  empresa = empresa ?? "[EMPRESA]"
  in18 = in18 ?? "en"

  return (
    <Html>
      <Head />
      <Preview>Log in with this magic link</Preview>
      <Body style={main}>
        <Container style={container}>
          <Img 
            src={`${baseURL}/${in18}/Header.png`}
            width="100%"
            height=""
            style={{
              margin: '0 auto',
            }}
            alt="Bienvenido a Beryllium"
          />
          <Container style={{
            margin: "0 40px",
            width: "fit-content"
          }}>
            <Row>
              <Column style={{
                width: "5%",
              }}/>
              <Column>
                <Heading style={heading}>
                  {
                    in18 == "es" ? "Hola, " :
                    in18 == "en" ? "Dear, " :
                    ""
                  } 
                  {empresa}
                </Heading>
                <Text style={{  ...text,
                  textAlign: "center",
                }}>
                  { 
                    in18 == "es" ? "Es un placer presentarles a Beryllium Development Company, una empresa especializada en desarrollo de software a medida, seguridad informática e infraestructura tecnológica. Nuestro propósito es brindar soluciones innovadoras que optimicen la gestión, refuercen la seguridad de la información y mejoren la eficiencia operativa de organizaciones como la suya." :
                    in18 == "en" ? "It is a pleasure to introduce Beryllium Development Company, a company specialized in custom software development, cybersecurity, and technology infrastructure. Our goal is to provide innovative solutions that optimize management, strengthen information security, and improve operational efficiency for organizations like yours." :
                    ""
                  }
                </Text> 
                <Row>
                  <Column style={{ width: "30%"}} />
                  <Column style={{ width: "40%"}} >
                    <Link
                      href="https://berylliumdev.com/#services"
                      style={{
                        textAlign: "center",
                        margin: "0 auto",
                      }}
                    >
                      <Img 
                        src={`${baseURL}/${in18}/_Services_Button_.png`}
                        height=""
                        style={{
                          margin: '0 auto',
                        }}
                        />
                    </Link>
                  </Column>
                  <Column style={{ width: "30%"}} />
                </Row>
                
                <Img 
                  src={`${baseURL}/${in18}/Body.png`}
                  width="100%"
                  height=""
                  style={{
                    margin: '15px auto',
                  }}
                  alt="Servicios de Beryllium"
                />
                <Text style={{  ...text,
                  textAlign: "center",
                }}>
                  { 
                    in18 == "es" ? "Adjuntamos nuestro brochure corporativo, donde encontrarán más detalles sobre nuestra experiencia y soluciones. Nos gustaría coordinar una reunión para explorar posibles oportunidades de colaboración. Quedamos atentos a su confirmación y agradecemos su tiempo e interés." :
                    in18 == "en" ? "We have attached our corporate brochure, where you will find more details about our experience and solutions. We would like to schedule a meeting to explore potential collaboration opportunities. We look forward to your confirmation and appreciate your time and interest." :
                    ""
                  }
                </Text>
                <Row>
                  <Column style={{ width: "35%"}} />
                  <Column style={{ width: "30%"}} >
                    <Link
                      href="https://drive.google.com/file/d/1Gba-aaVUsFkg16B2y3-E4F78nJEr_05W/view?usp=sharing"
                      style={{
                        textAlign: "center",
                        margin: "15px auto",
                      }}
                    >
                      {/* Ver Brochure */}
                      <Img 
                        src={`${baseURL}/${in18}/_Button_.png`}
                        height=""
                        style={{
                          margin: '15px auto',
                        }}
                        />
                    </Link>
                  </Column>
                  <Column style={{ width: "35%"}} />
                </Row>
              </Column>
              <Column style={{
                width: "5%",
              }}/>
            </Row>
            <Row>
              <Column style={{height: "20px"}}/>
            </Row>
          </Container>
          {/* Footer */}
          <Container style={{
            backgroundColor: "#000000",
            color: "white"
          }}>
            <Row>
              <Column style={{ height: "15px"}}/>
            </Row>
            <Row>
              <Column style={{ width: "5%" }}/>
              <Column style={{ width: "90%" }} >
                <Container style={{
                  width: "fit-content",
                  margin: "20px auto",
                }}>
                  <Row>
                    <Column style={{
                      width: "44%"
                    }}>
                      <Text>
                        {
                          in18 == "es" ? "Atentamente" : 
                          in18 == "en" ? "Sincerely" :
                          ""
                        }
                      </Text>
                      <Text style={{
                        fontWeight: "bold",
                        fontSize: "32px",
                      }}>
                        {/* CEO */}
                        Hiroshi Andre Chalco Peñafiel
                      </Text>
                      <Text>
                        {
                          in18 == "es" ? "Gerente General" : 
                          in18 == "en" ? "General Manager" :
                          ""
                        }
                      </Text>
                    </Column>
                    <Column style={{
                      backgroundColor: "black",
                      width:"2.5%"
                    }}/>
                    <Column style={{
                      backgroundColor: "white",
                      width:"1%"
                    }}/>
                    <Column style={{
                      backgroundColor: "black",
                      width:"2.5%"
                    }}/>
                    <Column style={{
                      width: "50%",
                    }}>
                      {/* <Row>
                        <Column>
                          <Img 
                            src={`${baseURL}/misc/Phone_Icon.png`}
                            width=""
                            height=""
                          />
                        </Column>
                        <Column >
                          <Text>
                          (+51) 974 444 461
                          </Text>
                        </Column>
                      </Row> */}
                      {rails.map((rail, index) => (
                        <Row key={index}>
                          <Column>
                            <Img 
                              src={`${baseURL}/misc/${rail.icon}`}
                              width=""
                              height=""
                            />
                          </Column>
                          <Column style={{ width: "5%" }}/>
                          <Column>
                            <Text style={{textAlign: "left"}}>
                              {rail.value}
                            </Text>
                          </Column>
                        </Row>
                      ))}
                    </Column>
                  </Row>
                </Container>   
              </Column>
              <Column style={{ width: "5%" }}/>
            </Row>
            <Row>
              <Column style={{ height: "15px"}}/>
            </Row>
            <Row>
              <Column style={{ width: "100%", textAlign: "center"}}>
                <Text>
                  { in18 == "es" ? "Visítanos en nuestra página web:" :
                    in18 == "en" ? "Visit us on our website:" :
                    ""
                  }
                </Text>
              </Column>
            </Row>
            <Row>
              <Column style={{ width: "37.5%"}}/>
              <Column>
                <Link
                  href="https://berylliumdev.com/"
                >
                  <Img 
                    src={`${baseURL}/${in18}/_Web_Button_.png`}
                    width=""
                    height=""
                  />
                </Link>
              </Column>
              <Column style={{ width: "37.5%"}}/>
            </Row>

            {/* <Row>
              <Column style={{ width: "100%", textAlign: "center"}}>
                <Text>
                  { in18 == "es" ? "Visítanos en nuestra página web:" :
                    in18 == "en" ? "Visit us on our website:" :
                    ""
                  }
                </Text>
              </Column>
            </Row> */}
            <Row>
              <Column style={{ width: "100%", textAlign: "center"}}>
                <Text>
                  { in18 == "es" ? "Síguenos en nuestras redes sociales:" :
                    in18 == "en" ? "Follow us on our social networks:" :
                    ""
                  }
                </Text>
              </Column>
            </Row>
            <Row>
            <Column style={{width:"33%"}}/>
              <Column>
                <Link
                  href="https://www.facebook.com/BerylliumDevCom"
                >
                  <Img 
                    src={`${baseURL}/misc/Facebook_Icon.png`}
                    width=""
                    height=""
                  />
                </Link>
              </Column>
              <Column style={{width:"2%"}}/>
              <Column>
                <Link
                  href="https://www.tiktok.com/@berylliumcompany"
                >
                  <Img 
                    src={`${baseURL}/misc/Tiktok_Icon.png`}
                    width=""
                    height=""
                  />
                </Link>
              </Column>
              <Column style={{width:"2%"}}/>
              <Column>
                <Link
                  href="https://www.instagram.com/berylliumcompany/"
                >
                  <Img 
                    src={`${baseURL}/misc/Instagram_Icon.png`}
                    width=""
                    height=""
                  />
                </Link>
              </Column>
              <Column style={{width:"2%"}}/>
              <Column>
                <Link
                  href="https://www.youtube.com/@BerylliumDevelopmentCompany"
                >
                  <Img 
                    src={`${baseURL}/misc/Youtube_Icon.png`}
                    width=""
                    height=""
                  />
                </Link>
              </Column>
              <Column style={{width:"33%"}}/>
            </Row>
            <Row>
              <Column style={{ height: "15px"}}/>
            </Row>
            <Row>
              <Column style={{width:"40%"}}/>
              <Column>
                <Img 
                  src={`${baseURL}/misc/Beryllium_Logo.png`}
                />
              </Column>
              <Column style={{width:"40%"}}/>
            </Row>
            <Row>
              <Column style={{width: "40%"}}/>
              <Column>
                <Link
                  href="https://berylliumdev.com/"
                  style={{
                    textAlign: "center",
                  }}
                >
                  <Text>
                    www.berylliumdev.com
                  </Text>
                </Link>
              </Column>
              <Column style={{width: "40%"}}/>
            </Row>
          </Container>
        </Container>
      </Body>
    </Html>

  )
}

const rails = [
  {
    icon: "Phone_Icon.png",
    value: "(+51) 974 444 461",
  },
  {
    icon: "Email_Icon.png",
    value: "administracion@berylliumdev.com",
  },
  {
    icon: "Location_Icon.png",
    value: "Calle Hipólito Unanue N°125, Urb Victoria, Cercado - Arequipa"
  },
  {
    icon: "RUC_Icon.png",
    value: "RUC: 20607340642"
  },
  {
    icon: "Person_Icon.png",
    value: "Beryllium Development Company S.A.C.",
  }
]

BerylliumEmailEmail.PreviewProps = {
  empresa: 'Beryllium',
  in18: 'en',
}

export default BerylliumEmailEmail;
